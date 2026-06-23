# PlantVillage 数据集下载说明

## 数据集简介

PlantVillage 数据集由宾夕法尼亚州立大学创建，是目前最广泛使用的农作物病害图像开源数据集之一。

| 属性 | 值 |
|------|-----|
| 总图片数 | 87,848 张 |
| 类别数量 | 38 类 |
| 作物种类 | 14 种 |
| 图片格式 | JPG |
| 图片尺寸 | 约 256×256 像素 |

## 下载方式

### 方式一：Kaggle（推荐）
1. 注册/登录 [Kaggle](https://www.kaggle.com)
2. 数据集地址：https://www.kaggle.com/datasets/abdallahalidev/plantvillage-dataset
3. 下载 `plantvillage dataset.zip` 后解压
4. 将 `plantvillage dataset/segmented/` 中的所有文件夹复制到本目录

### 方式二：使用 Kaggle CLI
```bash
pip install kaggle
kaggle datasets download -d abdallahalidev/plantvillage-dataset
unzip plantvillage-dataset.zip
```

## 目标目录结构

解压后应有如下结构：
```
data/PlantVillage/
├── Apple___Apple_scab/          (630张)
├── Apple___Black_rot/           (621张)
├── Apple___Cedar_apple_rust/    (275张)
├── Apple___healthy/             (1645张)
├── Blueberry___healthy/         (1502张)
├── Cherry_(including_sour)___Powdery_mildew/  (1052张)
├── Cherry_(including_sour)___healthy/         (854张)
... (共38个子目录)
```

## 验证数据集
```bash
py data/preprocess.py --check    # 检查完整性
py data/preprocess.py --analyze  # 统计分析
```
