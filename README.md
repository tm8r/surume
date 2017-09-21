# mayatools
オレオレmayaプラグインモジュールです。

# 利用方法
以下の場所にリポジトリ直下のmayatools.modを配置してください。  
Windows：C:¥Users¥ユーザー名¥Documents¥maya¥Mayaバージョン¥modules  
Mac : /Users/ユーザー名/Library/Preferences/Autodesk/maya/Mayaバージョン/modules  
※modulesディレクトリがなければ作成してください。

次に配置したmayatools.modをこのリポジトリの配置場所を書き換えてください。  
具体的には、mayatools.modは以下のような内容になっています。
```
+ MayaTools 1.0 /Users/tm8r/Documents/dev/mayatools
PYTHONPATH+:=python
```
この `/Users/tm8r/Documents/dev/mayatools` の部分をリポジトリの配置場所に書き換えてMayaを起動し、メニューバーにMayaToolsという項目があれば正常に動作しています:beers:
