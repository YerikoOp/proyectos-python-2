import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

def introducir_numero(mensaje,numeros_negativos = False):
    while True:
        numero_procesar = input(mensaje)
        try:
            numero = float(numero_procesar)
            if not numeros_negativos and numero <= 0:
                print (" no se permiten numeros negativos bro")
                continue
            return numero
        except ValueError:
            print ("Eso no es un numero valido")
            continue

def introducir_entero(mensaje,numeros_negativos = False):
    while True:
        numero_entero_procesar = input(mensaje)
        try:
            numero_entero = int(numero_entero_procesar)
            if not numeros_negativos and numero_entero <= 0:
                print (" no se permiten numeros negativos bro")
                continue
            return numero_entero
        except ValueError:
            print ("el brochacho realmente cree que eso es un entero 💀💀")
            continue


def valor_intrinseco(accion):
    try:
        FCFactual = accion.cashflow.loc["Free Cash Flow"].iloc[0]
    except KeyError:
        print("el flujo de caja libre de esta accion no esta disponible por lo que el programa no tiene exactitud :c")
        return None
    Tasa_crecimiento_estimada = introducir_numero("introduce la tasa de crecimiento estimada (del negocio): ")
    gNormal = Tasa_crecimiento_estimada / 100
    n = introducir_entero ("introduce el numero de años: ")
    Tasa_crecimiento_perpetuo = introducir_numero("introduce la tasa de crecimiento perpetuo: ")
    g = Tasa_crecimiento_perpetuo / 100
    tasa_descuento = introducir_numero("introduce tu tasa de descuento: ")
    r = tasa_descuento / 100
    
    FCn = FCFactual * ((1 + gNormal)**n)
    
    Vt = FCn * (1 + g) / (r - g)
    
    Vtd = Vt / ((1+r)**n)
    
    Flujo_efectivo_futuro = 0
    
    for t in range (1,n + 1):
        FCt = FCFactual * ((1 + gNormal)**t)
        Flujo_efectivo_futuro += FCt / ((1+r)**t)
    
    Valor_Intrinseco = Flujo_efectivo_futuro + Vtd
    return Valor_Intrinseco

def valor_por_accion(Valor_Intrinseco,accion,acciones):
    deuda_empresa_total = accion.info.get("totalDebt") or 0
    total_cash = accion.info.get("totalCash") or 0
    deuda_empresa_neta = deuda_empresa_total - total_cash
    valor_intrinseco_total_sindeuda = Valor_Intrinseco - deuda_empresa_neta
    if deuda_empresa_total == 0:
        print ("el la deuda total de la empresa no esta disponible por lo que los calculos no seran exactos :c")
    if total_cash == 0:
        print("el total cash de la empresa no esta disponible por lo que los calculos no seran exactos :c")
    return valor_intrinseco_total_sindeuda / acciones

def pedir_tickers():
    Tickers = []
    while True:
        entrada = input("Introduce el Ticker de la acción / escribe 'listo' para terminar: ")
        if entrada.lower() == "listo":
            break
        Tickers.append(entrada.upper())
    return Tickers

def screener():
    Tickers_procesar = pedir_tickers()
    Tickers = []
    for ticker in Tickers_procesar:
        ticker_procesado = yf.Ticker(ticker)
        Vi = valor_intrinseco(ticker_procesado)
        if Vi is None:
            print(f"No se pudo encontrar el valor intrinseco de {ticker}")
            continue
        Vr = ticker_procesado.info.get("marketCap")
        Va = valor_por_accion(Vi,ticker_procesado,ticker_procesado.info.get("sharesOutstanding")) # ahora pedire las acciones con un info get en lugar de hacerlo manual xd
        Var = ticker_procesado.info.get("currentPrice")
        Variación = ((ticker_procesado.info.get("currentPrice") - ticker_procesado.history(period="max")["High"].max()) / ticker_procesado.info.get("currentPrice")) * 100 #estuve un buen rato intentando hacer esta linea :V
        Tickers.append({
            "Ticker": ticker,
            "Valor_Intrinseco": Vi,
            "Valor_Real": Vr,
            "Valor_Intrinseco_Accion": Va,
            "Valor_Real_Accion": Var,
            "Variación": Variación,
        })
    ScreenerFrame = pd.DataFrame(Tickers)
    print(ScreenerFrame)

screener()
