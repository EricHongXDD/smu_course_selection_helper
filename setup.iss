; �ű��� Inno Setup �ű��� ���ɣ�
; �йش��� Inno Setup �ű��ļ�����ϸ��������İ����ĵ���

#define MyAppName "Smu_Course_Election_Helper"
#define MyAppVersion "2.0"
#define MyAppPublisher "Hong"
#define MyAppURL "https://github.com/EricHongXDD/smu_course_election_helper"
#define MyAppExeName "Smu_Course_Election_Helper_2.0.exe"

[Setup]
; ע: AppId��ֵΪ������ʶ��Ӧ�ó���
; ��ҪΪ������װ����ʹ����ͬ��AppIdֵ��
; (��Ҫ�����µ� GUID�����ڲ˵��е�� "����|���� GUID"��)
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
; ������ȡ��ע�ͣ����ڷǹ���װģʽ�����У���Ϊ��ǰ�û���װ����
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
; ע��: ��Ҫ���κι���ϵͳ�ļ���ʹ�á�Flags: ignoreversion��

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
 