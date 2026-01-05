# Documentación Técnica de la API: Autorización de Transacción (Process/Authorize)

**Fuente:** [APIs | izipay developers](https://developers.izipay.pe/api/#/operations/authorize_transaction)

---

## 1. Descripción General

El servicio de **Autorización de Transacción** (`Process/Authorize`) proporciona la funcionalidad para realizar la **autorización** o **pre-autorización** de una transacción. Su objetivo principal es verificar la validez y disponibilidad de los fondos, así como la autenticidad de la transacción, siendo un paso fundamental de seguridad antes de proceder con la transacción completa.

## 2. Endpoint

| Método | URL |
| :--- | :--- |
| `POST` | `https://testapi-pw.izipay.pe/authorization/api/Process/Authorize` |

## 3. Request

### 3.1. Headers

| Nombre | Tipo | Requerido | Descripción | Restricciones | Ejemplo |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `Authorization` | string | Sí | Token de autorización. | N/A | `123` |
| `transactionId` | string | Sí | ID único por cada transacción generada por el comercio. Debe ser el mismo que se envió al generar el token. | `>= 5` y `<= 40` caracteres | `16868479028040` |
| `Content-Type` | string | Sí | Tipo de contenido de la solicitud. | `application/json` | `application/json` |

### 3.2. Body (JSON)

El cuerpo de la solicitud es un objeto JSON que contiene los siguientes campos principales:

| Campo | Tipo | Requerido | Descripción | Valores Permitidos |
| :--- | :--- | :--- | :--- | :--- |
| `action` | string | Sí | Indicador de la forma de la compra. | `pay`, `pay_token`, `pay_token_external` |
| `merchantCode` | string | Sí | Código del comercio generado por Izipay. | `>= 7` y `<= 15` caracteres |
| `facilitatorCode` | string | No | Código de comercio generado por Izipay. | `>= 7` y `<= 15` caracteres |
| `language` | string | Sí | Idioma del mensaje de respuesta. | `ESP`, `ENG` |
| `urlIpn` | string | No | URL o API de notificación (IPN). | `>= 5` y `<= 400` caracteres |
| `order` | object | Sí | Objeto de la compra. | Ver **3.2.1. Objeto `order`** |
| `card` | object | No | Objeto con los datos de la tarjeta. **Nota:** Debe ser `null` si se usa `pay_token_external`. | Ver **3.2.2. Objeto `card`** |
| `token` | object | No | Objeto de Tokenización (Privada y Marca). | Ver **3.2.3. Objeto `token`** |
| `billing` | object | Sí | Objeto de la Facturación (tarjetahabiente). | Ver **3.2.4. Objeto `billing`** |
| `shipping` | object | No | Objeto del envío. | Ver **3.2.5. Objeto `shipping`** |
| `antifraud` | object | Sí | Objeto de nivel de riesgos. | Ver **3.2.6. Objeto `antifraud`** |
| `authentication` | object | No | Objeto de autenticación externa del tarjetahabiente. | Ver **3.2.7. Objeto `authentication`** |
| `customFields` | array[object] | No | Array de objetos personalizados (Máx. 10). | Ver **3.2.8. Objeto `customFields`** |

#### 3.2.1. Objeto `order` (Requerido)

| Campo | Tipo | Requerido | Descripción | Restricciones |
| :--- | :--- | :--- | :--- | :--- |
| `orderNumber` | string | Sí | Número de Pedido único por transacción. | `>= 5` y `<= 15` caracteres |
| `currency` | string | Sí | Moneda de la transacción. | `PEN`, `USD` |
| `amount` | string | Sí | Monto de la Txn. **Encriptado RSA**. | `>= 1` y `<= 400` caracteres (encriptado) |
| `installments` | string | No | Número de cuotas. | `00` a `36` |
| `deferred` | string | No | Número diferido. | `0`, `1`, `2`, `3` |
| `payMethod` | string | Sí | Indicador del método de pago. | `card`, `qr`, `apple_pay`, `yape_code`, `pago_push` |
| `channel` | string | Sí | Canal de origen de la operación. | `ecommerce`, `web`, `moto`, `mobile`, `recurrence`, `izivirtual` |
| `processType` | string | Sí | Tipo de proceso para `payMethod card`. | `autorize`, `preautorize`, `mitrecurrent` |
| `datetimeTerminalTransaction` | string | Sí | Fecha y Hora de la transacción (fecha actual). | `>= 10` y `<= 30` caracteres |
| `merchantBuyerId` | string | No | Identificador único del comprador. | `>= 6` y `<= 100` caracteres |

#### 3.2.2. Objeto `card` (Opcional/Condicional)

Los campos `pan`, `expirationMonth`, `expirationYear` y `cvc` deben ser **encriptados RSA** usando la Clave pública Izipay y expresados en Base64.

| Campo | Tipo | Requerido | Descripción | Restricciones |
| :--- | :--- | :--- | :--- | :--- |
| `brand` | string | No | Tipo de Marca de la tarjeta. | `MC`, `VS`, `AE`, `DN` |
| `pan` | string | Condicional | Número de tarjeta. | `>= 0` y `<= 400` caracteres (encriptado) |
| `expirationMonth` | string | Condicional | Mes de Expiración. | `>= 0` y `<= 400` caracteres (encriptado) |
| `expirationYear` | string | Condicional | Año de Expiración. | `>= 0` y `<= 400` caracteres (encriptado) |
| `cvc` | string | Condicional | Código de seguridad. | `>= 0` y `<= 400` caracteres (encriptado) |
| `cvcPresent` | string | No | Indicador de envío del CVC. | `SI`, `NO` |

#### 3.2.3. Objeto `token` (Opcional/Condicional)

**Nota Importante para `pay_token_external`:**
Si se usa `action: pay_token_external`, los campos `network`, `cryptogram`, `expirationMonthToken`, `expirationYearToken`, `requestorId`, `assuranceMethod` y `brand` son **obligatorios**. El objeto `card` debe ser `null`.

| Campo | Tipo | Requerido | Descripción | Restricciones |
| :--- | :--- | :--- | :--- | :--- |
| `cardToken` | string | Condicional | Valor token que identifica la tarjeta. **Obligatorio** para `action: pay_token`. | `>= 0` y `<= 64` caracteres |
| `buyerToken` | string | No | Valor token que identifica al cliente. | `>= 0` y `<= 64` caracteres |
| `cryptogram` | string | Condicional | Criptograma del token de red. **Obligatorio** para `pay_token_external` (no recurrente). | `>= 0` y `<= 255` caracteres |
| `expirationMonthToken` | string | Condicional | Mes de vencimiento del token. **Obligatorio** para `pay_token_external`. | `>= 0` y `<= 400` caracteres (encriptado) |
| `expirationYearToken` | string | Condicional | Año de vencimiento del token. **Obligatorio** para `pay_token_external`. | `>= 0` y `<= 400` caracteres (encriptado) |
| `network` | string | Condicional | Valor que identifica el token de red. **Obligatorio** para `pay_token_external`. | `>= 0` y `<= 400` caracteres (encriptado) |
| `cvc` | string | No | Código de verificación del token. | `>= 0` y `<= 400` caracteres (encriptado) |
| `requestorId` | string | Condicional | Identificador único del solicitante de token. **Obligatorio** para `pay_token_external`. | `>= 0` y `<= 11` caracteres |
| `assuranceMethod` | string | Condicional | Valor que indica la identificación y verificación. **Obligatorio** para `pay_token_external`. | `11`, `14`, `20`, `21`, `22`, `23`, `24` |
| `mitTransactionId` | string | Condicional | ID de la transacción inicial. **Obligatorio** para transacciones recurrentes (MIT). | `>= 0` y `<= 15` caracteres |
| `firstTransaction` | boolean | Condicional | Indicador de transacción inicial. **Obligatorio** para `pay_token_external`. | `true`, `false` |
| `wallet` | string | No | Identificador de la billetera. | `apple_pay`, `google_pay`, `samsung_pay` |

#### 3.2.4. Objeto `billing` (Requerido)

| Campo | Tipo | Requerido | Descripción | Restricciones |
| :--- | :--- | :--- | :--- | :--- |
| `firstName` | string | Sí | Nombres del tarjetahabiente. | `>= 2` y `<= 50` caracteres |
| `lastName` | string | Sí | Apellidos del tarjetahabiente. | `>= 2` y `<= 50` caracteres |
| `email` | string | Sí | Correo electrónico. | `>= 5` y `<= 50` caracteres |
| `phoneNumber` | string | Sí | Teléfono. | `>= 7` y `<= 15` caracteres |
| `street` | string | Sí | Dirección de facturación. | `>= 5` y `<= 40` caracteres |
| `postalCode` | string | Sí | Código Postal (CP). | `>= 5` y `<= 10` caracteres |
| `city` | string | Sí | Ciudad. | `>= 3` y `<= 40` caracteres |
| `state` | string | Sí | Departamento o estado. | `>= 3` y `<= 40` caracteres |
| `country` | string | Sí | País (Código ISO). | `2` caracteres |
| `documentType` | string | Sí | Tipo de documento de identidad. | `DNI`, `CE`, `PASAPORTE`, `RUC`, `OTROS` |
| `document` | string | Sí | Número de documento. | Varía según `documentType` |
| `companyName` | string | No | Nombre de la compañía. | `>= 1` y `<= 25` caracteres |

#### 3.2.5. Objeto `shipping` (Opcional)

Contiene los mismos campos que `billing` (`firstName`, `lastName`, `email`, `phoneNumber`, `street`, `postalCode`, `city`, `state`, `country`), pero son opcionales.

#### 3.2.6. Objeto `antifraud` (Requerido)

| Campo | Tipo | Requerido | Descripción | Restricciones |
| :--- | :--- | :--- | :--- | :--- |
| `clientIp` | string | Sí | Dirección IP de origen de la operación. | `>= 8` y `<= 20` caracteres |
| `deviceFingerPrintId` | string | Sí | ID del dispositivo (Thread Metrix). | `>= 1` y `<= 40` caracteres |
| `userScoring` | string | Sí | Usuario scoring (Token Session). | `>= 10` y `<= 20` caracteres |

#### 3.2.7. Objeto `authentication` (Opcional)

| Campo | Tipo | Requerido | Descripción | Restricciones |
| :--- | :--- | :--- | :--- | :--- |
| `auth3dsSli` | string | No | Indicador de nivel de seguridad. | `21`, `24` |
| `auth3dsUcafIndicator` | string | No | Valor ECI (resultado de autenticación). | `05`, `06`, `2`, `1`, `6`, `4`, `7` |
| `auth3dsStatus` | string | No | Indica si la transacción califica como autenticada. | `Y`, `A` |
| `auth3DSAAV` | string | No | Código criptográfico de autenticación (AAV/CAVV/AEVV). | `>= 0` y `<= 30` caracteres |
| `auth3dsSecureIndicator` | string | No | Versión del protocolo de autenticación. | `2` |
| `auth3dsTransactionId` | string | No | ID de transacción EMV 3DS. | `>= 0` y `<= 50` caracteres |
| `auth3dsXid` | string | No | Número único de Transacción de Comercio Electrónico Seguro. | `>= 0` y `<= 50` caracteres |

#### 3.2.8. Objeto `customFields` (Opcional)

Array de objetos con campos `name` y `value`. Los valores permitidos para `name` son `field1` a `field10`.

## 4. Response (200 Success)

Si la solicitud es exitosa, se devuelve un código de estado `200` con un cuerpo JSON.

| Campo | Tipo | Descripción | Ejemplo |
| :--- | :--- | :--- | :--- |
| `code` | string | Código de respuesta de la autorización. | `00` |
| `message` | string | Mensaje de respuesta de la autorización. | `Operación exitosa` |
| `messageUser` | string | Mensaje amigable para el usuario (ESP). | `Operación exitosa` |
| `messageUserEng` | string | Mensaje amigable para el usuario (ENG). | `Successful` |
| `response` | object | Objeto que contiene los detalles de la respuesta. | Ver **4.1. Objeto `response`** |
| `payloadHttp` | string | Mensaje original de respuesta utilizado para la generación de la firma. | `{"code":"00","message ...... "transactionId":"171053469122344"}` |
| `signature` | string | Hash del payload del request en Base64. | `G9T1rMf/axQYzkUsopaP/8+JncQTRaMmsfyfZswreTE=` |
| `transactionId` | string | ID único por cada transacción generada por el comercio. | `171053469122344` |

### 4.1. Objeto `response`

El objeto `response` contiene los objetos `order`, `card`, `billing`, `merchant`, `token`, `authentication` y `customFields` con los datos de la transacción procesada.

**Nota:** Si se usó `pay_token_external`, la respuesta incluirá campos específicos del token de red como `response.token.network`, `response.token.cryptogram`, `response.token.requestorId`, `response.token.assuranceMethod`, `response.token.mitTransactionId`, `response.token.cardNumberSuffix`, `response.token.brand` y `response.token.cardType`.

## 5. Códigos de Error

La documentación también menciona códigos de estado `4xx` (errores del cliente) y `500` (error del servidor), cuyos detalles específicos se encuentran en la sección de "Códigos y mensajes de respuesta" de la documentación de Izipay.

---

## 6. Ejemplo de Request (cURL)

```bash
curl --request POST \
  --url https://testapi-pw.izipay.pe/authorization/api/Process/Authorize \
  --header 'Accept: application/json' \
  --header 'Authorization: 123' \
  --header 'Content-Type: application/json' \
  --header 'transactionId: 16868479028040' \
  --data '{
  "action": "pay",
  "merchantCode": "4007701",
  "facilitatorCode": "6666041",
  "order": {
    "orderNumber": "ONTEST171094249",
    "currency": "PEN",
    "amount": "CocgZ4BcJQ7cPYA6WPm0jZbT0BTzL0ziHFxFglCXwI1hYjvJak9UGcNgjm12PuGvH3wvLVltFu+T1CRsLIb8EQJ48b2R3WGJq3PfvbVda/5u+2RwT4bWpJUY3PzKwpgNtG/bjoHEu9gxRhZi6+H/IYpwdYz9AuQi3sMsdA/Snla9C3yu5hdx+S3YWigQV/KAwjEQhu+/ZHUp+h23elQjt4hz4dX5iFv4l2vMeNmtCM6ZXqWSTBS7zy7UC6oDFZv3sDPo/XARgqp5R/snBNixtS7B5JxRdJ5/P1QwY3O7IVzgTt77MNUrRO/X7Nl3wRsVVI9NE08hk/bi8P9vhm824g==",
    "installments": "00",
    "deferred": "0",
    "payMethod": "card",
    "channel": "ecommerce",
    "processType": "autorize",
    "datetimeTerminalTransaction": "2024-02-21 18:55:38.547",
    "merchantBuyerId": "MC1767"
  },
  "card": {
    "brand": "MC",
    "pan": "o3ZzMaRkBUXxaamXGtdB43qKwmev8zX7ZZTvLgVjIzUHma+Z86W0zSc1czj5xjDh5oX4wNEXEr2JxciEg2QWhrcVSOYugXjfHLMxBNRA4+yvXAGXA4I8vonjLZ1xudsAF/cxR/HaIypuwH9l5dYHpaU56s4vkLGfSRxNkMWW2ETTe5DDDtNnzhicn99FhITaUdnjM4eIN7lR+pxbhpuN+F4Hn8pqcXK4eZORtCpD0bpy8iaIUGMGUcdPDpzpP2eZNHCnBKcjiCppfjyBaBq2Fc37gBKirnEYmJXoF6Er9PCzKqyoO0wm37z2Y5dfToFbTiAppV4SIddn/3JKaniSIg==",
    "expirationMonth": "l+qhcjeW+ZUiJfHrcVqaAghCeD1ZxRX701oqzU7/Il7mTc1K+y1sDmqa89CVyhSBYYvvCtVSjCtK5EzVV2bpWT7j0xD3/UiLAWBwpvsXW6WFwJHXoifQYr8IfSMTGw5a+y5RDC0mQCK8+oWS5V5cC3X3pEGMy45u/2Sto1kKE/lUM0dxqj5sa/MA9x5ZxH54BxRuAeCAN9emf4ICqhlUh4Sa+OYJhO08HoJKiKZWSLWkJWSIbOLJ+pObZ1Q+/3tyPiR/pSmPZbAhJzmBRxxM2mFN+yMqqA/uClV8kpGRPAwMfAtWiDZApcZ1ImIpmm+14VMaUT0vZ7D2bLaoYevGyQ==",
    "expirationYear": "EioP/dTua/OkT4xdnPvXaaHIE3kHACvT74LE1kWLrpP9AwCRCo89rEbmE76DAOtqt2w+n5CXSRJXG4Gw3EV5Jgyfr7/QHF1cMhH23RClV3aLm2XOU21OGZYE1qnejTxbzK2f3cv++iN6p1apFqDFc15/CekbuxzR7fiPPCN5Zbd4EAk8I6xRN6s30ZAFIOwQURrniuTsDxOLRkTVzzuxzG/A1JLpDbK5XXd72o16fNKeCA0z8SfUkt3pslStbVkYo0TWlN42MHki+MS0Ag==",
    "cvc": "WJCTtcm907Z9ttxtP0M68hoTZ7qqDaqfmBFJYqzpkcBnUCpSsyfsJG4HZ53Ily8G2FtSpwW9j6k7EWWMYnBjV/JJdXoW3Kf3EO0/CnQN1DHNz5sQjiGzXwKVI+dCHK8Lt60ElzHbxx/BbjW42Aq+o56XGQg16aH9lVU7MOPHBPLHwvHOEcMFSZE5QLJhvenYyz1TnoX+VEwwegFj4vn1H5P0jb79oR0Yu/SouDYTCQ2vhK1CXPKC924w9ZUsBxhnwp/y0uihheZ62OowdDPJjTOm8P5R4jzNGjYpmujk6rQb+ucSiA/EklGRHiM2W38rYS2TZVvtwSV+lZjqEPC0Pw==",
    "cvcPresent": "SI"
  },
  "token": {
    "cardToken": "",
    "buyerToken": "",
    "cryptogram": "",
    "expirationMonthToken": "",
    "expirationYearToken": ""
  },
  "billing": {
    "firstName": "Lucho",
    "lastName": "Torres",
    "email": "luchotorres@gmail.com",
    "phoneNumber": "989897960",
    "street": "Av. Jorge Chávez 275",
    "postalCode": "15000",
    "city": "Lima",
    "state": "Lima",
    "country": "PE",
    "documentType": "DNI",
    "document": "12345678",
    "companyName": "IziPruebas"
  },
  "shipping": {
    "firstName": "Juan",
    "lastName": "Pérez",
    "email": "juanperez@gmail.com",
    "phoneNumber": "989897960",
    "street": "Av. Jorge Chávez 275",
    "postalCode": "15000",
    "city": "Lima",
    "state": "Lima",
    "country": "PE"
  },
  "antifraud": {
    "clientIp": "192.168.1.1",
    "deviceFingerPrintId": "b10522b9-3bd2-46b2-b2c0-46f89bcf7183",
    "userScoring": "izipay_low"
  },
  "authentication": {
    "auth3dsSli": "21",
    "auth3dsUcafIndicator": "05",
    "auth3dsStatus": "Y",
    "auth3DSAAV": "jCQey09Yk4ctCBEAAA+8CQAAAAA=",
    "auth3dsSecureIndicator": "2",
    "auth3dsTransactionId": "15be19b8-fbf8-497a-b6dc-97e38a235d03",
    "auth3dsXid": "MDAwMDAwMDAwMDAwMDg1MzgwODg="
  },
  "language": "ESP",
  "urlIpn": "https://testapi-pw.izipay.pe/ipnclient/NotificationPublic/requests",
  "customFields": [
    { "name": "field1", "value": "campo1" },
    { "name": "field2", "value": "campo2" },
    { "name": "field3", "value": "campo3" },
    { "name": "field4", "value": "campo4" },
    { "name": "field5", "value": "campo5" },
    { "name": "field6", "value": "campo6" },
    { "name": "field7", "value": "campo7" },
    { "name": "field8", "value": "campo8" },
    { "name": "field9", "value": "campo9" },
    { "name": "field10", "value": "campo10" }
  ]
}'
```
