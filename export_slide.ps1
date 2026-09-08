
 = New-Object -ComObject PowerPoint.Application
 = .Presentations.Open((Resolve-Path 'test_slide5.pptx').Path, [Microsoft.Office.Core.MsoTriState]::msoTrue, [Microsoft.Office.Core.MsoTriState]::msoFalse, [Microsoft.Office.Core.MsoTriState]::msoFalse)
 = .Slides.Item(5)
.Export((Resolve-Path '.').Path + '\test_slide5.png', 'PNG', 1920, 1080)
.Close()
.Quit()
Write-Output 'Exported slide 5 to test_slide5.png'
