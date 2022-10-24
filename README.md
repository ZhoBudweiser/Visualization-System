# 领域方向综合设计：基于地形分割及拓扑关系构建的可视化系统实现



## 〇、要求

对规则格网数据，进行基于流域或分割算法进行分割，构建各个分割块之前的拓扑关系，并显示；
对规则格网数据，采用VTK构建地形模型的三维显示系统，实现缩放、旋转等功能；
对规则格网地形数据，实现淹没分析算法，并实现缩放、旋转等功能；
对散点数据，采用狄洛尼算法构建地形表面，采用VTK构建地形模型的三维显示系统，实现缩放、旋转等功能。



## 一、基本概念

### 1. 规则格网模型

规则网格通常是正方形、矩形、三角形等规则网格。规则网格将区域空间切分为规则的格网单元，每一个格网单元对应一个数值。数学上可以表示为一个矩阵，在计算机实现中则是一个二维数组。每个格网单元或数组的一个元素对应一个高程值。

对于规则网格中每个格网的数值有两种不同的解释。第一种是格网栅格观点，认为该格网单元的数值是其中所有点的高程值，即格网单元对应的地面面积内高程是均一的高度，这种数字高程模型是一个不连续的函数。第二种是点栅格观点认为该网格单元的数值是网格中心点的高程或该网格单元的平均高程值，这样就需要用一种插值方法来计算每个点的高程。

规则格网的高程矩阵，用计算机处理很容易，并且可以计算等高线、坡度、坡向和自动提取流域地形等，使得它成为DEM 使用最广泛的格式，许多国家提供的DEM 数据都是以规则格网的数据矩阵形式提供的。格网DEM 的缺点是:一是在地形简单区存在大量冗余数据; 二是如不改变格网大小，无法适用于起伏复杂程度不同的地区;三是对于某些特种计算如通视计算，过分依赖格网轴线，四是不能准确表示地形的结构和细部。为避免这些问题，可采用附加地形特征数据，如地形特征点、山骨线、谷底线、断裂线等，以描述地形结构。

### 2. VTK

VTK，全称为Visualization Toolkit，也就是可视化工具包。是一个开源、跨平台、可自由获取、支持并行处理的图形应用函数库。通过VTK可以将科学实验数据如建筑学、气象学、医学、生物学或者航空航天学，对体、面、光源等等的逼真渲染，从而帮助人们理解那些采取错综复杂而又往往规模庞大的数字呈现形式的科学概念或结果。

Python作为一种动态编程语言，它的变量没有类型，traits 库可以为python添加类型定义，可以认为traits是tvtk对象的属性。颜色属性虽然可以接受多样的值，却不是能接受所有的值，比如"abc"、0.5等等就不能很好地表示颜色。而且虽然为了方便用户使用，对外的接口可以接受各种各样形式的值，但是在内部必须有一个统一的表达方式来简化程序的实现。用Trait属性可以很好地解决这样的问题：它可以接受能表示颜色的各种类型的值；当给它赋值为不能表达颜色的值时，它能够立即捕捉到错误，并且提供一个有用的错误报告，告诉用户它能够接受什么样的值；它提供一个内部的标准的颜色表达方式

### 3.绘制技术

将长方体数据转化为三维图像，需要运用tvtk库的各种对象协调完成（管线）。具体包括：创建长方体对象tvtk.CubeSource；使用PloyDataMapper映射器，将数据转换为图形数据；创建一个Actor渲染器，将前者处理；创建一个Renderer，将Actor添加进去；创建一个RenderWindow(窗口)，将Renderer 添加进去；创建一个RenderWindowInteractor(窗口的交互工具)

TVTK库可读取的外部文件类型：.obj、.stl、.ply等。

读取stl文件的方法是：tvtk.STLReader(file_name = "文件名.stl")

读取MutiBlock数据的方法是：tvtk.MultiBlockPLOT3DReader(fname1,fname2,m,n)，fname1:Plot 3D 网格（XYZ文件），fname2:气动力学结果(Q文件)，m:标量数据数，n:矢量数据数

### 4.管线技术

TVTK的管线包括两部分：可视化管线(Visualization Pipeline)：将原始数据加工成图形数据的过程。包括数据、数据预处理、数据映射。图形管线(Graphics Pipeline)：图形数据加工为我们所看到的图像的过程。包括数据映射、绘制、显示。

### 5.数据集

ImageData： 正交等距网格 表示二维或三维图像的数据结构；在数组中存放数据，点位于正交且等距的网格上，我们不需要给出坐标，点之间的连接是隐性的；

RectilinearGrid：非等距正交网格 所有点都在正交但不等间距的网格上，由于是非等距的，所以需要规定点坐标；

StructuredGrid：任意形状的网格 可以创建任意形状的网格，需要指定点的坐标；

PolyData：点，点之间的联系和点构成的多边形 即前述创建三维对象实例所用的数据集。由一系列的点、点之间的联系以及由点构成的多边形组成。

UnstructuredGrid： 任意分布的点以及它们的区域面积

### 6.可视化方法

在标量数据可视化实例中，创建等值面对象的方法是generate_values()和set_value()。generate_values()方法中的两个参数的意义为指定轮廓数和数据范围。set_value()的参数值会产生指定等值面和对应的等值面的值。
