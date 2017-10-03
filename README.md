# surume
オレオレmayaプラグインモジュールです。

# 利用方法
以下の場所にリポジトリ直下のsurume.modを配置してください。  
Windows：C:¥Users¥ユーザー名¥Documents¥maya¥Mayaバージョン¥modules  
Mac : /Users/ユーザー名/Library/Preferences/Autodesk/maya/Mayaバージョン/modules  
※modulesディレクトリがなければ作成してください。

次に配置したsurume.modをこのリポジトリの配置場所を書き換えてください。  
具体的には、surume.modは以下のような内容になっています。
```
+ surume 1.0 /Users/tm8r/Documents/dev/surume
PYTHONPATH+:=python
```
この `/Users/tm8r/Documents/dev/surume` の部分をリポジトリの配置場所に書き換えてMayaを起動し、メニューバーにsurumeという項目があれば正常に動作しています:beers:
