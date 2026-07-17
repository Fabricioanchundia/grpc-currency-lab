import grpc
import currency_pb2
import currency_pb2_grpc
import time

def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = currency_pb2_grpc.CurrencyConverterStub(channel)

    # 1) Obtener monedas soportadas (server-stream)
    print("Monedas soportadas:")
    try:
        for currency in stub.GetSupportedCurrencies(currency_pb2.Empty()):
            print(f" - {currency.code}: {currency.name}")
    except grpc.RpcError as e:
        print("Error GetSupportedCurrencies:", e)

    # 2) Ejemplo de Convert (unary)
    req = currency_pb2.ConvertRequest(from_currency="USD", to_currency="EUR", amount=100.0)
    try:
        reply = stub.Convert(req)
        print(f"\nConvert {req.amount} {req.from_currency} -> {reply.converted_amount:.4f} {req.to_currency} (rate={reply.rate})")
    except grpc.RpcError as e:
        print("Convert error:", e)

    # 3) Escuchar StreamRates por 5 elementos (server stream)
    print("\nStream de tasas (ejemplo, 5 items):")
    try:
        stream = stub.StreamRates(currency_pb2.Empty())
        for i, item in enumerate(stream):
            print(f" {i+1}) {item.from_currency} -> {item.to_currency} : rate={item.rate}")
            if i >= 4:
                break
    except grpc.RpcError as e:
        print("StreamRates error:", e)

    # 4) Desafío: GetRate (solo la tasa, sin convertir cantidad)
    print("\nGetRate (desafío):")
    rate_req = currency_pb2.RateRequest(from_currency="EUR", to_currency="GBP")
    try:
        rate_reply = stub.GetRate(rate_req)
        print(f" Tasa {rate_req.from_currency} -> {rate_req.to_currency}: {rate_reply.rate}")
    except grpc.RpcError as e:
        print("GetRate error:", e)

    # 4b) GetRate con una moneda no soportada, para probar el manejo de errores
    print("\nGetRate con moneda no soportada (prueba de error):")
    rate_req_bad = currency_pb2.RateRequest(from_currency="USD", to_currency="JPY")
    try:
        rate_reply_bad = stub.GetRate(rate_req_bad)
        print(f" Tasa {rate_req_bad.from_currency} -> {rate_req_bad.to_currency}: {rate_reply_bad.rate}")
    except grpc.RpcError as e:
        print(f" Error esperado -> status: {e.code()}, detalle: {e.details()}")

    # 5) Actividad: Suma (RPC unary de ejemplo)
    print("\nSuma (actividad):")
    suma_req = currency_pb2.SumaRequest(a=15, b=27)
    try:
        suma_reply = stub.Suma(suma_req)
        print(f" {suma_req.a} + {suma_req.b} = {suma_reply.resultado}")
    except grpc.RpcError as e:
        print("Suma error:", e)


if __name__ == "__main__":
    run()
