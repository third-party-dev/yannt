pip install mypackage --extra-index-url https://gitlab.com/api/v4/projects/PROJECT_ID/packages/pypi/simple

# pip.conf
[global]
extra-index-url = https://gitlab.com/api/v4/projects/PROJECT_ID/packages/pypi/simple


pip install -r https://gitlab.com/user/repo/-/raw/main/requirements.txt


```
# requirements.txt in gitlab

# direct wheels from the same repo
https://oauth2:TOKEN@gitlab.com/user/repo/-/raw/main/dist/package_a-1.0-py3-none-any.whl
https://oauth2:TOKEN@gitlab.com/user/repo/-/raw/main/dist/package_b-1.0-py3-none-any.whl

# regular pypi packages resolved implicitly
requests
click
pydantic>=2.0
```

Put packages in gitlab repo and point at it in requirements.txt

```
--extra-index-url https://gitlab.com/api/v4/projects/PROJECT_ID/packages/pypi/simple

package_a
package_b
requests
```