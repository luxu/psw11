from django.contrib import messages
from django.contrib.messages import constants
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect

from empresarios.models import Empresas, Documento
from investidores.models import PropostaInvestimento


def sugestao(request):
    if not request.user.is_authenticated:
        return redirect("/usuarios/logar")
    areas = Empresas.area_choices
    if request.method == 'GET':
        return render(
            request,
            'sugestao.html',
            {'areas': areas}
        )
    elif request.method == 'POST':
        tipo = request.POST.get('tipo')
        area = request.POST.getlist('area')
        valor = request.POST.get('valor')
        if tipo == 'C':
            empresas = Empresas.objects.filter(tempo_existencia='+5').filter(estagio='E')
        elif tipo == 'D':
            empresas = Empresas.objects.filter(tempo_existencia__in=['-6', '-6', '+1']).exclude(estagio='E')
        # TODO: Tipo genérico (Sem ser CONSERVADOR ou DISPOJADO nome MEDIANO)
        empresas = empresas.filter(area__in=area)

        empresas_selecionadas = []
        for empresa in empresas:
            percentual = (float(valor) * 100) / float(empresa.valuation)
            if percentual >= 1:
                empresas_selecionadas.append(empresa)
        return render(
            request,
            'sugestao.html',
            {'areas': areas, 'empresas': empresas_selecionadas}
        )


def ver_empresa(request, id):
    empresa = Empresas.objects.get(id=id)
    documentos = Documento.objects.filter(empresa=empresa)
    proposta_investimento = (PropostaInvestimento.objects
                              .filter(empresa=empresa)
                              .filter(status='PA')
                              )
    percentual_vendido = 0
    for pi in proposta_investimento:
        percentual_vendido += pi.percentual

    limiar = (80 * empresa.percentual_equity) / 100
    concretizado = False
    if percentual_vendido >= limiar:
        concretizado = True

    percentual_disponivel = empresa.percentual_equity - percentual_vendido

    # TODO: Listar as métricas dinamicamente
    return render(
        request,
'ver_empresa.html',
{
            'empresa': empresa,
            'documentos': documentos,
            'percentual_vendido': int(percentual_vendido),
            'concretizado': concretizado,
            'percentual_disponivel': int(percentual_disponivel)
        }
    )


def realizar_proposta(request, id):
    valor = request.POST.get('valor')
    percentual = request.POST.get('percentual')
    empresa = Empresas.objects.get(id=id)

    propostas_aceitas = (
        PropostaInvestimento.objects
        .filter(empresa=empresa)
        .filter(status='PA')
    )
    total = 0
    for pa in propostas_aceitas:
        total += pa.percentual

    if total + float(percentual) > empresa.percentual_equity:
        messages.add_message(
            request,
            constants.WARNING,
            'O percentual solicitado ultrapassa o percentual máximo'
        )
        return redirect(f'/investidores/ver_empresa/{id}')

    valuation = ((int(valor) * 100)) / int(percentual)

    if valuation < (int(empresa.valuation / 2)):
        messages.add_message(
            request,
            constants.WARNING,
            f'Seu valuation proposto foi R${valuation} e deve ser no mínimo {empresa.valuation}'
        )
        return redirect(f'/investidores/ver_empresa/{id}')

    pi = PropostaInvestimento(
        valor=valor,
        percentual=percentual,
        empresa=empresa,
        investidor=request.user,
    )

    pi.save()
    return redirect(f'/investidores/assinar_contrato/{pi.id}')


def assinar_contrato(request, id):
    pi = PropostaInvestimento.objects.get(id=id)
    if pi.status != 'AS':
        raise Http404()
    if request.method == "GET":
        return render(request, 'assinar_contrato.html', {'id': id, 'pi': pi})

    elif request.method == "POST":
        selfie = request.POST.get('selfie')
        rg = request.POST.get('rg')

        pi.selfie = selfie
        pi.rg = rg
        pi.status = 'PE'
        pi.save()
        messages.add_message(
            request,
            constants.WARNING,
            'Contrato assinado com sucesso, sua proposta foi enviada para a empresa!'
        )
        return redirect(f'/investidores/ver_empresa/{pi.empresa.id}')
