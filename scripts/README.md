# strip_tones.py — 生成去除拼音声调数字的词库副本

简短说明：本脚本用于从词库文件中移除拼音后面的声调数字（1–4），并生成一个去掉声调数字的副本，方便在不支持声调标注的输入法中使用。

文件位置
- `scripts/strip_tones.py`

快速使用（Windows PowerShell）
- 生成默认输出（若输入文件名以 `-terra` 结尾，输出名会去掉该段；否则在原名后加 `-notone`）：
```powershell
python .\scripts\strip_tones.py .\sjy-keng-kyim-qyim-khawq-terra.dict.yaml
```
- 指定输出文件名：
```powershell
python .\scripts\strip_tones.py -o .\sjy-keng-kyim-qyim-khawq.dict.yaml .\sjy-keng-kyim-qyim-khawq-terra.dict.yaml
```
- 就地替换（会先创建 `.bak` 备份）：
```powershell
python .\scripts\strip_tones.py -i .\sjy-keng-kyim-qyim-khawq-terra.dict.yaml
```
- 批量处理当前目录下所有 `.dict.yaml`：
```powershell
Get-ChildItem -Filter *.dict.yaml | ForEach-Object { python .\scripts\strip_tones.py $_.FullName }
```

实现细节与注意事项
- 正则策略：脚本仅移除紧跟在 ASCII 字母序列后的数字 `1-4`（例如 `jun1` → `jun`）。这样可以避免误删独立数字（例如日期、版本号）。
- 编码：脚本以 UTF-8 读写文件；如果你的文件使用不同编码，请先转换或联系我来添加编码选项。
- 文件命名：默认行为会把输入文件名中尾部的 `-terra` 删除（以满足本仓库命名偏好）；若输入不含 `-terra`，脚本会在文件名后加 `-notone` 以避免覆盖原文件。
- 扩展：如果你的拼音包含 `ü`、`ǖ` 等非 ASCII 字母或使用特殊转写（例如 `v` 代替 `ü`），我可以把正则扩展为匹配 Unicode 字母。

自动化建议（可选）
- 在 CI 中加入一步，自动生成去声调版本并发布到 release 或同步到需要的目录。示例（GitHub Actions）大致思路：checkout → setup python → run `python scripts/strip_tones.py` → upload artifact。
- 若想在本地提交时自动刷新去声调版本，可以在本机设置 `.git/hooks/pre-commit`（或使用 husky 之类的工具）运行脚本并把生成的文件加入到提交。

如果你希望我：
- 把这个 README 合并到主 README 的指定段落；或
- 添加一个简单的 GitHub Actions CI 文件示例；或
- 扩展脚本以支持 Unicode 拼音（例如 `ü`），请告诉我，我会继续实现。
