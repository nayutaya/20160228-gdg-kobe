
# README

2016年2月28日開催されたGDG神戸 機械学習勉強会での発表資料とそのソースコード。

## イベント

[GDG神戸 機械学習勉強会 [AlphaGoの論文を読む会] - GDG神戸 | Doorkeeper](https://gdgkobe.doorkeeper.jp/events/39169)

## スライド

[TensorFlowを使ってテキストをクラス分類してみた](http://www.slideshare.net/YuyaKato3/tensorflow-58795721)

## AWS EC2における環境構築

```
# タイムゾーンを日本時間に変更
sudo sed -i -e "s/^ZONE=.*/ZONE=\"Asia\/Tokyo\"/" /etc/sysconfig/clock
sudo ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime

# ホスト名を変更
sudo sed -i -e "s/^HOSTNAME=.*/HOSTNAME=ec2-r3-xlarge/" /etc/sysconfig/network

sudo reboot

# Python3、pipをインストール
sudo yum update
sudo yum install -y python34-devel python34-pip
python3 --version
> Python 3.4.3
pip-3.4 --version
> pip 6.1.1 from /usr/lib/python3.4/dist-packages (python 3.4)

# 依存ライブラリをインストール
sudo yum install -y gcc-c++ git ruby rubygem-rake
sudo pip-3.4 install janome mojimoji msgpack-python more-itertools
> Successfully installed janome-0.2.6 mojimoji-0.0.5 more-itertools-2.2 msgpack-python-0.4.7
sudo pip-3.4 install --upgrade https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-0.7.1-cp34-none-linux_x86_64.whl
> Successfully installed numpy-1.10.4 protobuf-3.0.0b2 setuptools-20.1.1 six-1.10.0 tensorflow-0.7.1 wheel-0.29.0
```
