# build_deploy.ps1
# ---------------------------------------------------------------------------
# ONE-COMMAND rebuild for canvas_parent_api:
#   1. deletes stale build/ + egg-info + dist artifacts
#   2. builds a fresh wheel from src/ (src layout -> no stale copies possible)
#   3. verifies the wheel ACTUALLY contains the current code
#      (enrollment_state on courses(), the label kwarg, the per-call logger)
#   4. optionally deploys the wheel into the Open WebUI container and verifies
#      what is imported at runtime (not just the version metadata)
#
# Usage:
#   pwsh build_deploy.ps1                      # build + deploy to "open-webui"
#   pwsh build_deploy.ps1 -Container my-owui   # different container name
#   pwsh build_deploy.ps1 -NoDeploy            # build + verify only, no docker
#
# NOTE: if Open WebUI re-installs the tool from the GitHub master.zip
# (tool requirement line), you must ALSO push these changes to GitHub so the
# zip no longer contains a stale build/ folder.
# ---------------------------------------------------------------------------
param(
    [string]$Container = "open-webui",
    [switch]$NoDeploy
)

$ErrorActionPreference = "Stop"
Set-Location (Split-Path -Parent $PSCommandPath)

Write-Host "== 1/4 cleaning stale build artifacts =="
Remove-Item -Recurse -Force "build", "dist", "src\canvas_parent_api.egg-info", "canvas_parent_api.egg-info" -ErrorAction SilentlyContinue

Write-Host "== 2/4 building wheel from src/ =="
py -m pip wheel . --no-deps -w dist
$wheel = Get-ChildItem "dist\*.whl" | Select-Object -First 1
if (-not $wheel) { throw "no wheel produced in dist/" }
Write-Host "built: $($wheel.Name)"

Write-Host "== 3/4 verifying wheel contains current code =="
py -c "import glob, zipfile, sys; w=glob.glob(r'dist/*.whl')[0]; z=zipfile.ZipFile(w); c=z.read('canvas_parent_api/canvas.py').decode(); cl=z.read('canvas_parent_api/canvas_api_client.py').decode(); checks={'courses enrollment_state': 'enrollment_state' in c.split('async def courses')[1].split(chr(10))[0], 'label kwarg': 'label: str = None' in c, 'log_request': 'def _log_request' in cl, 'log_response': 'def _log_response' in cl, 'planner_items': 'def get_planner_items' in cl, 'planner model': 'canvas_parent_api/models/planner_item.py' in z.namelist(),
        'planner schema': all(k in z.read('canvas_parent_api/models/base.py').decode() for k in ('plannable_type', 'plannable_date', 'plannable'))}; [print(('PASS  ' if v else 'FAIL  ') + k) for k, v in checks.items()]; sys.exit(0 if all(checks.values()) else 1)"

Write-Host "== 4/4 deploy =="
if ($NoDeploy) {
    Write-Host "deployment skipped (-NoDeploy)."
} elseif (Get-Command docker -ErrorAction SilentlyContinue) {
    docker cp "$($wheel.FullName)" "${Container}:/tmp/$($wheel.Name)"
    docker exec $Container pip install --force-reinstall "/tmp/$($wheel.Name)"
    docker exec $Container python -c "import inspect; from importlib.metadata import version; from canvas_parent_api import Canvas; print('installed version:', version('canvas_parent_api')); print('courses signature:', inspect.signature(Canvas.courses))"
    Write-Host "deployed + runtime-verified into container '$Container'."
} else {
    Write-Host "docker CLI not available here. On the docker host run:"
    Write-Host "  docker cp `"$($wheel.FullName)`" ${Container}:/tmp/$($wheel.Name)"
    Write-Host "  docker exec $Container pip install --force-reinstall /tmp/$($wheel.Name)"
    Write-Host "  docker exec $Container python -c `"import inspect; from canvas_parent_api import Canvas; print(inspect.signature(Canvas.courses))`""
}
Write-Host "done."