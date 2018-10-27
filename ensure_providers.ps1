
function Invoke-Nuget {
    $nuget = (gcm .\nuget.exe -EA 0);
    if (-not $nuget) {
        $nuget = (gcm nuget.exe -EA 0);
    }
    if (-not $nuget) {
        iwr https://aka.ms/nugetclidl -outfile .\nuget.exe;
        $nuget = (gcm .\nuget.exe -EA 0);
    }
    if (-not $nuget) {
        throw "Failed to locate nuget.exe. Cannot install providers"
    }
    & $nuget $args
    return ""
}

pushd ($MyInvocation.MyCommand.Definition | Split-Path -Parent)
try {
    Invoke-Nuget restore .\packages.config -O downloads
    gci "downloads\*.exe" -r | %{ copy $_ "azure_devops_keyring" }
} finally {
    popd
}
