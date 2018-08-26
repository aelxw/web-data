Attribute VB_Name = "Functions"

Public Sub startServer()
Call Shell(runServerPath)
If Not sheetExists(conSheetSettlement) Then
    setup
End If
End Sub

Public Sub stopServer()
Dim req As New MSXML2.ServerXMLHTTP60
Dim server As String
Dim url As String
server = "http://localhost:9999"
url = server & "/shutdown"
req.Open "GET", url
req.send
End Sub

Public Sub loadSettlement()
ThisWorkbook.Sheets(conSheetSettlement).Activate
initDateForm
settlement (DateForm.loadText.Value)
End Sub

Public Sub loadGen()
ThisWorkbook.Sheets(conSheetGen).Activate
initDateForm
gen (DateForm.loadText.Value)
End Sub

Public Sub loadHoep()
ThisWorkbook.Sheets(conSheetHoep).Activate
initDateForm
hoep (DateForm.loadText.Value)
End Sub

Public Sub loadWeather()
ThisWorkbook.Sheets(conSheetWeather).Activate
initDateForm
weather (DateForm.loadText.Value)
End Sub

Public Sub setup()

Dim settlementSheet As Worksheet
Set settlementSheet = ThisWorkbook.Sheets.Add(After:=ThisWorkbook.Sheets(ThisWorkbook.Sheets.Count))
settlementSheet.Name = conSheetSettlement
Values = Array("tradeDate", "market", "price", "currency", "uom", "month")
settlementSheet.Range("A1", Cells(1, UBound(Values) + 1)) = Values

Dim genSheet As Worksheet
Set genSheet = ThisWorkbook.Sheets.Add(After:=ThisWorkbook.Sheets(ThisWorkbook.Sheets.Count))
genSheet.Name = conSheetGen
Values = Array("date", "source", "hour", "capability", "output")
genSheet.Range("A1", Cells(1, UBound(Values) + 1)) = Values

Dim hoepSheet As Worksheet
Set hoepSheet = ThisWorkbook.Sheets.Add(After:=ThisWorkbook.Sheets(ThisWorkbook.Sheets.Count))
hoepSheet.Name = conSheetHoep
Values = Array("date", "hour", "price")
hoepSheet.Range("A1", Cells(1, UBound(Values) + 1)) = Values

Dim weatherSheet As Worksheet
Set weatherSheet = ThisWorkbook.Sheets.Add(After:=ThisWorkbook.Sheets(ThisWorkbook.Sheets.Count))
weatherSheet.Name = conSheetWeather
Values = Array("day", "month", "place", "name", "hdd", "cdd", "minTemp", "meanTemp", "maxTemp")
weatherSheet.Range("A1", Cells(1, UBound(Values) + 1)) = Values

End Sub

Function sheetExists(sheetToFind As String) As Boolean
    sheetExists = False
    For Each Sheet In Worksheets
        If sheetToFind = Sheet.Name Then
            sheetExists = True
            Exit Function
        End If
    Next Sheet
End Function

Public Sub initDateForm()
DateForm.loadText.Value = Format(Now(), "yyyyMMdd")
DateForm.Show
End Sub
