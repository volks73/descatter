; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "Descatter"
#define MyAppVersion "0.0.1"
#define MyAppPublisher "Christopher R. Field"
#define MyAppURL "https://github.com/volks73/descatter"
#define MyAppExeName "descatter-console.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{2D70485F-02A6-4DA1-A83F-243E0AF564C0}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={pf}\{#MyAppName}
DefaultGroupName={#MyAppName}
LicenseFile=C:\Users\cfield\Code\Eclipse\descatter\build\exe.win-amd64-3.3\LICENSE
OutputDir=C:\Users\cfield\Code\Eclipse\descatter\build\installer
OutputBaseFilename=descatter_install
Compression=lzma
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64
ArchitecturesAllowed=x86 x64
UninstallDisplayName={#MyAppName} {#MyAppVersion}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 0,6.1

[Files]
Source: "C:\Users\cfield\Code\Eclipse\descatter\build\exe.win-amd64-3.3\descatter-console.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cfield\Code\Eclipse\descatter\build\exe.win-amd64-3.3\_bz2.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cfield\Code\Eclipse\descatter\build\exe.win-amd64-3.3\_hashlib.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cfield\Code\Eclipse\descatter\build\exe.win-amd64-3.3\_lzma.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cfield\Code\Eclipse\descatter\build\exe.win-amd64-3.3\_socket.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cfield\Code\Eclipse\descatter\build\exe.win-amd64-3.3\_ssl.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cfield\Code\Eclipse\descatter\build\exe.win-amd64-3.3\AUTHORS"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cfield\Code\Eclipse\descatter\build\exe.win-amd64-3.3\CHANGES"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cfield\Code\Eclipse\descatter\build\exe.win-amd64-3.3\descatter.ini"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cfield\Code\Eclipse\descatter\build\exe.win-amd64-3.3\descatter-cmd.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cfield\Code\Eclipse\descatter\build\exe.win-amd64-3.3\LICENSE"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cfield\Code\Eclipse\descatter\build\exe.win-amd64-3.3\lxml.etree.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cfield\Code\Eclipse\descatter\build\exe.win-amd64-3.3\lxml.objectify.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cfield\Code\Eclipse\descatter\build\exe.win-amd64-3.3\pyexpat.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cfield\Code\Eclipse\descatter\build\exe.win-amd64-3.3\python33.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cfield\Code\Eclipse\descatter\build\exe.win-amd64-3.3\README.rst"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cfield\Code\Eclipse\descatter\build\exe.win-amd64-3.3\select.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cfield\Code\Eclipse\descatter\build\exe.win-amd64-3.3\unicodedata.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\cfield\Code\Eclipse\descatter\build\exe.win-amd64-3.3\directives\*"; DestDir: "{app}\directives"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
