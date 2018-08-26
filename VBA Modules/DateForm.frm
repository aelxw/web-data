VERSION 5.00
Begin {C62A69F0-16DC-11CE-9E98-00AA00574A4F} DateForm 
   Caption         =   " Date Form"
   ClientHeight    =   735
   ClientLeft      =   120
   ClientTop       =   465
   ClientWidth     =   4905
   OleObjectBlob   =   "DateForm.frx":0000
   StartUpPosition =   1  'CenterOwner
End
Attribute VB_Name = "DateForm"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False


Private Sub loadText_KeyDown(ByVal KeyCode As MSForms.ReturnInteger, ByVal Shift As Integer)
If KeyCode = 13 Then
DateForm.loadText.Value = DateForm.loadText.Value
DateForm.Hide
End If
End Sub

Private Sub UserForm_QueryClose(Cancel As Integer, CloseMode As Integer)
initDateForm
DateForm.loadText.Value = DateForm.loadText.Value
End Sub
