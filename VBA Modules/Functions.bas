Attribute VB_Name = "Functions"

Public Sub startServer()
setup
Call Shell(conRunServerPath)
End Sub

Public Sub stopServer()
Dim req As New MSXML2.ServerXMLHTTP60
Dim server As String
Dim url As String
url = conServer & "/shutdown"
req.Open "GET", url
req.send
End Sub

Public Sub loadSettlement()
ThisWorkbook.Sheets(conSheetSettlement).Activate
If initDateForm Then
    settlement (DateForm.loadText.Value)
End If
End Sub

Public Sub loadGen()
ThisWorkbook.Sheets(conSheetGen).Activate
If initDateForm Then
    gen (DateForm.loadText.Value)
End If
End Sub

Public Sub loadHoep()
ThisWorkbook.Sheets(conSheetHoep).Activate
If initDateForm Then
    hoep (DateForm.loadText.Value)
End If
End Sub

Public Sub loadWeather()
ThisWorkbook.Sheets(conSheetWeather).Activate
If initDateForm Then
    weather (DateForm.loadText.Value)
End If
End Sub

Public Sub setup()

Dim settlementSheet As Worksheet
If sheetExists(conSheetSettlement) Then
    Set settlementSheet = ThisWorkbook.Worksheets(conSheetSettlement)
Else
    Set settlementSheet = ThisWorkbook.Sheets.Add(After:=ThisWorkbook.Sheets(ThisWorkbook.Sheets.Count))
    settlementSheet.Name = conSheetSettlement
End If
Values = Array("tradeDate", "market", "price", "currency", "uom", "month")
settlementSheet.Range("A1", Cells(1, UBound(Values) + 1).Address) = Values

Dim genSheet As Worksheet
If sheetExists(conSheetGen) Then
    Set genSheet = ThisWorkbook.Worksheets(conSheetGen)
Else
    Set genSheet = ThisWorkbook.Sheets.Add(After:=ThisWorkbook.Sheets(ThisWorkbook.Sheets.Count))
    genSheet.Name = conSheetGen
End If
Values = Array("date", "source", "hour", "capability", "output")
genSheet.Range("A1", Cells(1, UBound(Values) + 1).Address) = Values

Dim hoepSheet As Worksheet
If sheetExists(conSheetHoep) Then
    Set hoepSheet = ThisWorkbook.Worksheets(conSheetHoep)
Else
    Set hoepSheet = ThisWorkbook.Sheets.Add(After:=ThisWorkbook.Sheets(ThisWorkbook.Sheets.Count))
    hoepSheet.Name = conSheetHoep
End If
Values = Array("date", "hour", "price")
hoepSheet.Range("A1", Cells(1, UBound(Values) + 1).Address) = Values

Dim weatherSheet As Worksheet
If sheetExists(conSheetWeather) Then
    Set weatherSheet = ThisWorkbook.Worksheets(conSheetWeather)
Else
    Set weatherSheet = ThisWorkbook.Sheets.Add(After:=ThisWorkbook.Sheets(ThisWorkbook.Sheets.Count))
    weatherSheet.Name = conSheetWeather
End If
Values = Array("day", "month", "place", "name", "hdd", "cdd", "minTemp", "meanTemp", "maxTemp")
weatherSheet.Range("A1", Cells(1, UBound(Values) + 1).Address) = Values

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

Public Function initDateForm() As Boolean
initDateForm = False
DateForm.loadText.Value = Format(Now(), "yyyyMMdd")
DateForm.Show
If Len(DateForm.loadText.Value) = 8 Then
    initDateForm = True
End If
End Function
