Attribute VB_Name = "MarketData"

Public Function getJsonData(endpoint As String, param As String) As String
Dim req As New MSXML2.ServerXMLHTTP60
Dim server As String
Dim url As String
url = conServer & endpoint & "?date=" & param
req.Open "GET", url
req.send
getJsonData = req.responseText
End Function

Public Sub jsonToWorksheet(JsonString As String, sht As Worksheet, header() As Variant)
Dim json As Collection
Set json = ParseJson(JsonString)
Application.ScreenUpdating = False
Application.Calculation = xlCalculationManual
sht.Range("A2", sht.Cells(1000000, UBound(header, 2))).Clear
i = 2
For Each Item In json
    For j = 1 To UBound(header, 2)
        sht.Cells(i, j).Value = Item(header(1, j))
    Next
    i = i + 1
Next
Application.ScreenUpdating = True
Application.Calculation = xlCalculationAutomatic
End Sub

Public Sub settlement(param As String)
Dim jsonData As String
Dim header() As Variant
jsonData = getJsonData(conEndpointSettlement, param)
Dim sht As Worksheet
Set sht = ThisWorkbook.Sheets(conSheetSettlement)
Dim col As Integer
col = sht.Range("A1").End(xlToRight).Column
header = sht.Range("A1", sht.Cells(1, col)).Value
jsonToWorksheet jsonData, ThisWorkbook.Sheets(conSheetSettlement), header
End Sub

Public Sub gen(param As String)
Dim jsonData As String
Dim header() As Variant
jsonData = getJsonData(conEndpointGen, param)
Dim sht As Worksheet
Set sht = ThisWorkbook.Sheets(conSheetGen)
Dim col As Integer
col = sht.Range("A1").End(xlToRight).Column
header = sht.Range("A1", sht.Cells(1, col)).Value
jsonToWorksheet jsonData, ThisWorkbook.Sheets(conSheetGen), header
End Sub

Public Sub hoep(param As String)
Dim jsonData As String
Dim header() As Variant
jsonData = getJsonData(conEndpointHoep, param)
Dim sht As Worksheet
Set sht = ThisWorkbook.Sheets(conSheetHoep)
Dim col As Integer
col = sht.Range("A1").End(xlToRight).Column
header = sht.Range("A1", sht.Cells(1, col)).Value
jsonToWorksheet jsonData, ThisWorkbook.Sheets(conSheetHoep), header
End Sub

Public Sub weather(param As String)
Dim jsonData As String
Dim header() As Variant
jsonData = getJsonData(conEndpointWeather, param)
Dim sht As Worksheet
Set sht = ThisWorkbook.Sheets(conSheetWeather)
Dim col As Integer
col = sht.Range("A1").End(xlToRight).Column
header = sht.Range("A1", sht.Cells(1, col)).Value
jsonToWorksheet jsonData, ThisWorkbook.Sheets(conSheetWeather), header
End Sub

