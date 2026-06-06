Imports System.IO

Public Class Form1
    Private Sub Form1_Load(sender As Object, e As EventArgs) Handles MyBase.Load
        Label1.Text = ""
        Dim ScreenWidth As Integer = Screen.PrimaryScreen.Bounds.Width
        Dim ScreenHeight As Integer = Screen.PrimaryScreen.Bounds.Height
        Left = ScreenWidth - Width - 50
        Top = ScreenHeight - Height - 75
    End Sub

    Private Sub Timer1_Tick(sender As Object, e As EventArgs) Handles Timer1.Tick
        Try
            Label1.Text = File.ReadAllText("dockLog.txt")
            If Label1.Text = "EXIT" Then
                File.WriteAllText("dockLog.txt", "")
                Close()
            End If
        Catch ex As Exception

        End Try
    End Sub

    Private Sub Label1_Click(sender As Object, e As EventArgs) Handles Label1.Click

    End Sub
End Class
