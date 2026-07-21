; Pomodoro Timer Installer -- NSIS Script
Unicode true

!include "MUI2.nsh"

Name "Pomodoro Timer"
OutFile "installer\PomodoroTimer_Setup_v1.0.0.exe"
InstallDir "$PROGRAMFILES64\Pomodoro Timer"
RequestExecutionLevel admin

!define MUI_ABORTWARNING

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

!insertmacro MUI_LANGUAGE "SimpChinese"
!insertmacro MUI_LANGUAGE "English"

Section "Install"
  SetOutPath "$INSTDIR"
  ExecWait 'taskkill /f /im PomodoroTimer.exe' $0

  File "dist\PomodoroTimer.exe"
  File "README.md"

  CreateDirectory "$SMPROGRAMS\Pomodoro Timer"
  CreateShortCut "$SMPROGRAMS\Pomodoro Timer\Pomodoro Timer.lnk" "$INSTDIR\PomodoroTimer.exe"
  CreateShortCut "$SMPROGRAMS\Pomodoro Timer\Uninstall.lnk" "$INSTDIR\uninst.exe"
  CreateShortCut "$DESKTOP\Pomodoro Timer.lnk" "$INSTDIR\PomodoroTimer.exe"

  WriteUninstaller "$INSTDIR\uninst.exe"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\PomodoroTimer" \
    "DisplayName" "Pomodoro Timer"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\PomodoroTimer" \
    "UninstallString" "$INSTDIR\uninst.exe"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\PomodoroTimer" \
    "DisplayVersion" "1.0.0"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\PomodoroTimer" \
    "Publisher" "VirginiaH233"
SectionEnd

Section "Uninstall"
  ExecWait 'taskkill /f /im PomodoroTimer.exe' $0
  Delete "$INSTDIR\PomodoroTimer.exe"
  Delete "$INSTDIR\README.md"
  Delete "$INSTDIR\uninst.exe"
  RMDir "$INSTDIR"
  Delete "$SMPROGRAMS\Pomodoro Timer\Pomodoro Timer.lnk"
  Delete "$SMPROGRAMS\Pomodoro Timer\Uninstall.lnk"
  RMDir "$SMPROGRAMS\Pomodoro Timer"
  Delete "$DESKTOP\Pomodoro Timer.lnk"
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\PomodoroTimer"
SectionEnd
