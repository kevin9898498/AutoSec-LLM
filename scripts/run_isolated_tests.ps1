[CmdletBinding()]
param(
    [string]$Image = "llm-secure-repair-tests",
    [switch]$BuildOnly
)

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Push-Location $ProjectRoot
try {
    docker build --tag $Image --file Dockerfile.test .
    if (-not $BuildOnly) {
        # Network-off plus resource limits keep the benchmark tests separated
        # from the host. tmpfs gives pytest a small writable temp directory.
        docker run --rm --network none --read-only --tmpfs /tmp:rw,noexec,nosuid,size=64m `
            --memory 512m --cpus 1.0 --pids-limit 128 --security-opt no-new-privileges `
            $Image
    }
}
finally {
    Pop-Location
}
