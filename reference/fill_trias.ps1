# Fill the empty trias template with trias_case.json and save Excel's recalculated copy.
# Needs Microsoft Excel; only run to regenerate trias_reference_case.xlsx.
$ErrorActionPreference = 'Stop'
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$case = Get-Content -Raw (Join-Path $here 'trias_case.json') | ConvertFrom-Json
$template = Join-Path $here 'Finanzplan_Wohnprojekte_Stiftung_trias.xlsx'
$out = Join-Path $here 'trias_reference_case.xlsx'

$xl = New-Object -ComObject Excel.Application
$xl.Visible = $false
$xl.DisplayAlerts = $false
try {
    $wb = $xl.Workbooks.Open($template, 0, $true)
    # Sheet positions in the template: 6 building 1, 8 capital and financing, 9 financial plan.
    $building = $wb.Worksheets.Item(6)
    $capital = $wb.Worksheets.Item(8)
    $plan = $wb.Worksheets.Item(9)

    $building.Range('F8').Value2 = [double]$case.rent_per_m2_month
    $building.Range('G8').Value2 = [double]$case.private_area_m2
    $building.Range('H8').Value2 = [double]1
    $building.Range('G20').Value2 = [double]$case.common_area_m2
    $building.Range('H20').Value2 = [double]1
    $building.Range('F32').Value2 = [double]$case.maintenance_per_m2_year
    $building.Range('F33').Value2 = [double]$case.vacancy_rate
    $building.Range('F34').Value2 = [double]$case.inflation

    $plan.Range('I2').Value2 = [double]$case.inflation
    $plan.Range('F36:J36').Value2 = [double]$case.admin_cost_per_year
    $plan.Range('F46:J46').Value2 = [double]$case.insurance_per_year
    $plan.Range('F80').Value2 = -[double]$case.investment

    $capital.Range('F7').Value2 = [double]$case.equity
    $capital.Range('F43').Value2 = [double]$case.direct_loan.amount
    $capital.Range('E48').Value2 = [double]$case.direct_loan.interest_rate
    $capital.Range('E68').Value2 = [double]$case.bank_loan.amount
    $capital.Range('E69').Value2 = [double]$case.bank_loan.term_years
    $capital.Range('E70').Value2 = [double]0
    $capital.Range('E72').Value2 = [double]1
    $capital.Range('E82').Value2 = [double]$case.bank_loan.interest_rate
    $capital.Range('E110').Value2 = [double]$case.subsidy_loan.amount
    $capital.Range('E111').Value2 = [double]$case.subsidy_loan.term_years
    $capital.Range('E112').Value2 = [double]0
    $capital.Range('E114').Value2 = [double]1
    $capital.Range('E124').Value2 = [double]$case.subsidy_loan.interest_rate

    $xl.CalculateFull()
    $wb.SaveAs($out, 51)
    $wb.Close($false)
    Write-Output "wrote $out"
}
finally {
    $xl.Quit()
    [void][Runtime.InteropServices.Marshal]::ReleaseComObject($xl)
}
