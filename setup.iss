; 脚本由 Inno Setup 脚本向导 生成！
; 有关创建 Inno Setup 脚本文件的详细资料请查阅帮助文档！

#define MyAppName "Smu_Course_Election_Helper"
#define MyAppVersion "2.0"
#define MyAppPublisher "Hong"
#define MyAppURL "https://github.com/EricHongXDD/smu_course_election_helper"
#define MyAppExeName "Smu_Course_Election_Helper_2.0.exe"

[Setup]
; 注: AppId的值为单独标识该应用程序。
; 不要为其他安装程序使用相同的AppId值。
; (若要生成新的 GUID，可在菜单中点击 "工具|生成 GUID"。)
AppId={{C2892DC2-B752-4549-A3AD-C7BB18FACAC1}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DisableProgramGroupPage=yes
InfoBeforeFile=C:\Users\10292\PycharmProjects\smu_course_election_helper\dist\license.txt
InfoAfterFile=C:\Users\10292\PycharmProjects\smu_course_election_helper\dist\finish.txt
; 以下行取消注释，以在非管理安装模式下运行（仅为当前用户安装）。
;PrivilegesRequired=lowest
OutputDir=C:\Users\10292\Desktop
OutputBaseFilename=Smu_Course_Election_Helper_Setup
SetupIconFile=C:\Users\10292\PycharmProjects\smu_course_election_helper\logo.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "chinesesimp"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "C:\Users\10292\PycharmProjects\smu_course_election_helper\dist\Smu_Course_Election_Helper_2.0\Smu_Course_Election_Helper_2.0.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\10292\PycharmProjects\smu_course_election_helper\dist\Smu_Course_Election_Helper_2.0\_internal\*"; DestDir: "{app}\_internal"; Flags: ignoreversion recursesubdirs createallsubdirs
; 注意: 不要在任何共享系统文件上使用“Flags: ignoreversion”

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
 