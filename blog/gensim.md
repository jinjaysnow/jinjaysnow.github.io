title:   GenSim
authors: Jin Jay
Date:    2015-11
description: Gensim, Python文档处理库，用于机器学习等数据预处理。
keywords: Gensim
          Python
          Tf-Idf
          LSA
          LDA
          RP
          机器学习
          文本处理


# Gensim文档

Gensim是一个免费的用来自动提取文档主题的Python库。特点：

+ 内存独立，没有必要一次把所有的训练语料库载入内容。
+ 对几个流行的向量空间算法进行了高效的实现，包括**Tf-Idf**, **Latent Semantic Analysis**, **Latent Dirichlet Allocation**, **Random Projection**;添加一个新的也非常容易。
+ 对几个流行的数据格式进行了IO包装和转换。
+ 实现了文档相似度查询

安装：
```sh
pip install gensim
```

## 语料库和向量空间

使用以下代码来记录日志：

```Python
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
```

### 将字符串转为向量

示例：
```Python
from gensim import corpora, models, similarities

documents = ["Human machine interface for lab abc computer applications",
             "A survey of user opinion of computer system response time",
             "The EPS user interface management system",
             "System and human system engineering testing of EPS",
             "Relation of user perceived response time to error measurement",
             "The generation of random binary unordered trees",
             "The intersection graph of paths in trees",
             "Graph minors IV Widths of trees and well quasi ordering",
             "Graph minors A survey"]
```

需要先将每一行文档进行预处理，得到token字符，去掉不必要的字符

```Python
>>> # 去除字符中得空格等
>>> stoplist = set('for a of the and to in'.split())
>>> texts = [[word for word in document.lower().split() if word not in stoplist]
>>>          for document in documents]
>>>
>>> # 将只出现一次的单词移除
>>> from collections import defaultdict
>>> frequency = defaultdict(int)
>>> for text in texts:
>>>     for token in text:
>>>         frequency[token] += 1
>>>
>>> texts = [[token for token in text if frequency[token] > 1]
>>>          for text in texts]
>>>
>>> from pprint import pprint   # 更好的输出格式
>>> pprint(texts)
[['human', 'interface', 'computer'],
 ['survey', 'user', 'computer', 'system', 'response', 'time'],
 ['eps', 'user', 'interface', 'system'],
 ['system', 'human', 'system', 'eps'],
 ['user', 'response', 'time'],
 ['trees'],
 ['graph', 'trees'],
 ['graph', 'minors', 'trees'],
 ['graph', 'minors', 'survey']]
```

当然，处理文档的方式有很多种；这里只是简单的将空格移除，然后将每一个单词小写。处理文档的方式太多也太有针对性，所以在这一方面并没有限制。一个文档代表的是从它里面可以提取出特征，怎样获得特征由你决定。下面介绍一种通用的方法，词袋(bag-of-words)，但是需要记住，不同的应用需要不同的特征，而且，garbage in, garbage out(输入了垃圾数据，便会输出垃圾结果)。。。

为了将文档转化为向量，我们需要使用一个文档表示方法——词袋(bag-of-words)。每一个文档通过一个向量来表示，每一个向量都表示一个QA(question-answer)对，如下

> "How many times does the word system appear in the document? Once."

使用整型id来表示问题是十分有利的。问题和id之间的映射成为一个词典(dictionary):
```Python
>>> dictionary = corpora.Dictionary(texts)
>>> dictionary.save('/tmp/deerwester.dict') # 保存以备之后使用
>>> print(dictionary)
Dictionary(12 unique tokens)
```

这里我们给在语料库中的每一个单词分配了一个整型id，通过`gensim.corpora.dictionary.Dictionary`类。这一步会对文本进行清理，对文本计数，并作一些相关的统计。最后，我们能够发现在处理后的语料库中有12个的单独的单词，表示每一个文档能够通过这12个数字来表示(也即12维向量)。为了可视化单词和他们的id之间的映射，可以通过print来查看。

```Python
>>> print(dictionary.token2id)
{'minors': 11, 'graph': 10, 'system': 5, 'trees': 9, 'eps': 8, 'computer': 0,
'survey': 4, 'user': 7, 'human': 1, 'time': 6, 'interface': 2, 'response': 3}
```

实际中我们可以这样将文档转为向量：
```Python
>>> new_doc = "Human computer interaction"
>>> new_vec = dictionary.doc2bow(new_doc.lower().split())
>>> print(new_vec) # 单词"interaction"并没有在词袋中，我们将它舍弃
[(0, 1), (1, 1)]
```

此处函数`doc2bow()`简单的计算每一个单词出现的数量，将单词与整型id结合返回一个向量。向量`[(0,1),(1,1)]`表示，在文档`Human computer interaction`中，单词`computer`(id为0)和`human`(id为1)只出现了一次；其他的单词出现0次。

```Python
>>> corpus = [dictionary.doc2bow(text) for text in texts]
>>> corpora.MmCorpus.serialize('/tmp/deerwester.mm', corpus) # store to disk, for later use
>>> print(corpus)
[(0, 1), (1, 1), (2, 1)]
[(0, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
[(2, 1), (5, 1), (7, 1), (8, 1)]
[(1, 1), (5, 2), (8, 1)]
[(3, 1), (6, 1), (7, 1)]
[(9, 1)]
[(9, 1), (10, 1)]
[(9, 1), (10, 1), (11, 1)]
[(4, 1), (10, 1), (11, 1)]
```

### 语料库流，一次处理一个文档
上面的例子中，语料库完全保存在内存中，作为一个python的list对象。在这个简单的例子中，这并不重要，但是为了使事情更清晰，我们假设有语料库中有上百万个文档。内容不能完全存储这么多的内容。所以，假设文档保存在磁盘中，一个文档一行。Gensim允许每一次只处理一个文档，并返回一个文档向量。

```Python
>>> class MyCorpus(object):
>>>     def __iter__(self):
>>>         for line in open('mycorpus.txt'):
>>>             # 假设一行一个文档，文档通过空格来分别单词
>>>             yield dictionary.doc2bow(line.lower().split())
```

可以尝试自己更改`__iter__`方法，来解析文档，生成单词列表，然后转化为词典。

```Python
>>> corpus_memory_friendly = MyCorpus() # doesn't load the corpus into memory!
>>> print(corpus_memory_friendly)
<__main__.MyCorpus object at 0x10d5690>
```

现在语料库是一个对象。我们还没有定义任何的方法来输出它，所以print只会显示对象在内存中的地址。并不十分有用。为了看到组成向量。我们可以在语料库上进行迭代并打印文档向量。
```Python
>>> for vector in corpus_memory_friendly: # load one vector into memory at a time
...     print(vector)
[(0, 1), (1, 1), (2, 1)]
[(0, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
[(2, 1), (5, 1), (7, 1), (8, 1)]
[(1, 1), (5, 2), (8, 1)]
[(3, 1), (6, 1), (7, 1)]
[(9, 1)]
[(9, 1), (10, 1)]
[(9, 1), (10, 1), (11, 1)]
[(4, 1), (10, 1), (11, 1)]
```

尽管输出类似于纯的python列表，但是现在语料库是内存友好的，因为每一次最多有一个向量在内容中。现在语料库可以尽可能的大了。

同样，也可以不加载所有文本到内存来构造词典：

```Python
>>> # 获取token的统计信息
>>> dictionary = corpora.Dictionary(line.lower().split() for line in open('mycorpus.txt'))
>>> # 去掉停止字符和那些只出现一次的单词
>>> stop_ids = [dictionary.token2id[stopword] for stopword in stoplist
>>>             if stopword in dictionary.token2id]
>>> once_ids = [tokenid for tokenid, docfreq in dictionary.dfs.iteritems() if docfreq == 1]
>>> dictionary.filter_tokens(stop_ids + once_ids) # 移除停止词和出现一次的词
>>> dictionary.compactify() # 在移除无用的词后消除id序列的间隔
>>> print(dictionary)
Dictionary(12 unique tokens)
```

接下来，我们还需要面对这个问题：这些不同的单词中如何计算出有用的频率信息？我们需要在这个词典的表示上应用一些变换，在我们能够使用它来计算有意义的文档相似性之前。后面我们会讲解变换，下面我们来看看语料库持久化。

### 语料库格式
由多种文件格式可以选择来序列化一个向量空间的语料库到本地磁盘。Gensim通过流语料库接口来实现：文档采用懒惰读取，一次一个文档，不用一次读取全部内容。

其中一种文件格式是[Market Matrix fomat](http://math.nist.gov/MatrixMarket/formats.html)。采用这个来保存语料库如下：
```Python
>>> from gensim import corpora
>>> # 创建一个有两个文档的示例语料库
>>> corpus = [[(1, 0.5)], []]  # 是其中一个文档为空，来看看它的魔力
>>>
>>> corpora.MmCorpus.serialize('/tmp/corpus.mm', corpus)
```

其他的格式包括[Joachim's SVMlight format](http://svmlight.joachims.org/), [Blei's LDA-C format](http://www.cs.princeton.edu/~blei/lda-c/),[GibblesLDA++ format](http://gibbslda.sourceforge.net/)。

```Python
>>> corpora.SvmLightCorpus.serialize('/tmp/corpus.svmlight', corpus)
>>> corpora.BleiCorpus.serialize('/tmp/corpus.lda-c', corpus)
>>> corpora.LowCorpus.serialize('/tmp/corpus.low', corpus)
```
相对地，从一个matrix market 文件中加载语料库迭代器：
```Python
>>> corpus = corpora.MmCorpus('/tmp/corpus.mm')
```

Corpus对象是一种流，所以不可以直接打印输出信息：
```Python
>>> print(corpus)
MmCorpus(2 documents, 2 features, 1 non-zero entries)
```

查看信息：
```Python
>>> # 一个输出corpus的方法:将它全部加载进内存
>>> print(list(corpus)) # 调用list()方法会是所有的序列变为纯的python列表
[[(1, 0.5)], []]
```
或者：
```Python
>>> # another way of doing it: print one document at a time, making use of the streaming interface
>>> for doc in corpus:
...     print(doc)
[(1, 0.5)]
[]
```

很显然第二种方法更加内存友好。

可以使用如下代码使用Blei's LDA-C格式来保存相同的Matrix Market文档流。
```Python
>>> corpora.BleiCorpus.serialize('/tmp/corpus.lda-c', corpus)
```

这样，gensim也能够用来作为一个高效内存的IO格式转化工具：使用一种格式加载文档流然后直接使用另外一种格式保存。

### 与NumPy和SciPy兼容
Gensim包含了一些高效的工具函数来帮助与numpy数据格式进行相互转换。
```Python
>>> corpus = gensim.matutils.Dense2Corpus(numpy_matrix)
>>> numpy_matrix = gensim.matutils.corpus2dense(corpus, num_terms=number_of_corpus_features)
```

也能够与scipy进行相互转换。
```Python
>>> corpus = gensim.matutils.Sparse2Corpus(scipy_sparse_matrix)
>>> scipy_csc_matrix = gensim.matutils.corpus2csc(corpus)
```

## 主题与转换

### 转换接口
继续上一节的内容，先加载语料库：

```Python
>>> from gensim import corpora, models, similarities
>>> dictionary = corpora.Dictionary.load('/tmp/deerwester.dict')
>>> corpus = corpora.MmCorpus('/tmp/deerwester.mm')
>>> print(corpus)
MmCorpus(9 documents, 12 features, 28 non-zero entries)
```
下面演示如何将文档从一个向量空间转换到另一个。这个过程有两个目标：
1. 显现我们语料库的隐藏结构，找到词与词之间的关系，并使用他们以更加语义化的方式来描述新的文档。
2. 使文档表示更加坚实。包括提升效率(新表示方法需要更少的资源)和功效(去除无效的数据，降噪)。

### 创建一个变换
变换是一个标准的Python对象，通常从一个训练的语料库中初始化。
```Python
>>> tfidf = models.TfidfModel(corpus) # 步骤1，初始化一个模型
```
使用我们之前的语料库来初始化一个变换模型。不同的变换可能需要不同的初始化参数；就`Tfidf`方法而言，训练的组成包扩遍历一遍提供的语料库和计算文档的所有特征的频率。训练其他的模型，比如`Latent Semantic Analysis`或者`Latent Dirichlet Allocation`，需要更深入的同时更多次的遍历。

> 注：变换总是在两个特定的向量空间之间进行。必须使用相同的向量空间(也就是特征id相同)来训练和进行子向量变换。使用相同的输入特征空间会导致错误，比如应用一个不同的字符创处理函数，使用不同的特征id，或者在应该使用Tfidf向量的时候使用了词袋向量，这些都会使得变换过程中特征不匹配，最终导致garbage out或者运行时异常。

### 转换向量
到此，`tfidf`被作为一个只读的对象，能够将任意的一个向量从旧的表示方法(词袋)转换为一个新的表示(Tfidf真值权重)。
```Python
>>> doc_bow = [(0, 1), (1, 1)]
>>> print(tfidf[doc_bow]) # 步骤2，使用模型来转换向量
[(0, 0.70710678), (1, 0.70710678)]
```
后者，在整个语料库上进行转换：
```Python
>>> corpus_tfidf = tfidf[corpus]
>>> for doc in corpus_tfidf:
...     print(doc)
[(0, 0.57735026918962573), (1, 0.57735026918962573), (2, 0.57735026918962573)]
[(0, 0.44424552527467476), (3, 0.44424552527467476), (4, 0.44424552527467476), (5, 0.32448702061385548), (6, 0.44424552527467476), (7, 0.32448702061385548)]
[(2, 0.5710059809418182), (5, 0.41707573620227772), (7, 0.41707573620227772), (8, 0.5710059809418182)]
[(1, 0.49182558987264147), (5, 0.71848116070837686), (8, 0.49182558987264147)]
[(3, 0.62825804686700459), (6, 0.62825804686700459), (7, 0.45889394536615247)]
[(9, 1.0)]
[(9, 0.70710678118654746), (10, 0.70710678118654746)]
[(9, 0.50804290089167492), (10, 0.50804290089167492), (11, 0.69554641952003704)]
[(4, 0.62825804686700459), (10, 0.45889394536615247), (11, 0.62825804686700459)]
```

在这个特定的例子中，我们能够转化之前用于训练的相同的语料库，但是结果是次要的。一旦变换模型被初始化，它就可以用在任何向量上(当然，假定他们来自相同的向量空间),即使没有在训练的语料库中使用过。这通过LSA中被称为`folding-in`过程实现。

> 注：调用`model[corpus]`只会创建一个对旧的数据流的包装，真正的变换是在文档迭代的过程中飞速完成的。我们不能在调用`corpus_transformed=model[corpus]`时转换所有的语料库，因为这意味着保存结果到内存中，与gensim的内存独立相违背。如果需要多次迭代变换`corpus_transformed`,然后转换的开销很大，可以先将其序列化到磁盘上，然后继续使用。

转换可以序列化，在一条链上：
```Python
>>> lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=2) # 初始化一个LSI变换
>>> corpus_lsi = lsi[corpus_tfidf] # 在原来的语料库上创建两个包装，bow->tfidf->fold-in-lsi
```
上面我们通过[Latent Semantic Indexing](http://en.wikipedia.org/wiki/Latent_semantic_indexing)将tf-idf语料库转换为一个二维空间(我们设定num_topics=2)。现在，有可能好奇：这两个维度代表什么？我们可以看一下它的内部：
```Python
>>> lsi.print_topics(2)
topic #0(1.594): -0.703*"trees" + -0.538*"graph" + -0.402*"minors" + -0.187*"survey" + -0.061*"system" + -0.060*"response" + -0.060*"time" + -0.058*"user" + -0.049*"computer" + -0.035*"interface"
topic #1(1.476): -0.460*"system" + -0.373*"user" + -0.332*"eps" + -0.328*"interface" + -0.320*"response" + -0.320*"time" + -0.293*"computer" + -0.280*"human" + -0.171*"survey" + 0.161*"trees"
```
(topic信息被打印到日志中)

根据LSI，"trees", "graph", "minors"是所有的相关的单词(并且在首要主题上的贡献最大)，而第二个主题与所有的其他词都相关联。正如期待的那样，前五个文档与第二个主题是足够相关的，而剩下的与第一个主题相关。
```Python
>>> for doc in corpus_lsi: # bow->tfidf和tfidf->lsi变换都会在这里快速执行
...     print(doc)
[(0, -0.066), (1, 0.520)] # "Human machine interface for lab abc computer applications"
[(0, -0.197), (1, 0.761)] # "A survey of user opinion of computer system response time"
[(0, -0.090), (1, 0.724)] # "The EPS user interface management system"
[(0, -0.076), (1, 0.632)] # "System and human system engineering testing of EPS"
[(0, -0.102), (1, 0.574)] # "Relation of user perceived response time to error measurement"
[(0, -0.703), (1, -0.161)] # "The generation of random binary unordered trees"
[(0, -0.877), (1, -0.168)] # "The intersection graph of paths in trees"
[(0, -0.910), (1, -0.141)] # "Graph minors IV Widths of trees and well quasi ordering"
[(0, -0.617), (1, 0.054)] # "Graph minors A survey"
```

模型的持久化使用save()和load()函数：
```Python
>>> lsi.save('/tmp/model.lsi') # same for tfidf, lda, ...
>>> lsi = models.LsiModel.load('/tmp/model.lsi')
```

下一个问题是：两个文档是如何相似的？是否存在一个方法来确定相似度，对于一个给定的输入文档，我们可以根据相似度来处理其它的文档？下一节我们会介绍相似度。

### 可使用的变换
Gensim包含一些流行的向量空间模型算法：

+ [Term Frequency \* Inverse Document Frequency, Tf-Idf](http://en.wikipedia.org/wiki/Tf–idf)接受词袋训练向量来初始化。在变换过程中，可以将一个向量转换为相同维度的向量，使得训练数据中的稀有特征的值得到增加。它最后将整型的向量转换为实数值，保留数字的维度不变。也可以可选地归一化结果向量为单位长度。
```Python
>>> model = tfidfmodel.TfidfModel(bow_corpus, normalize=True)
```
+ [Latent Semantic Indexing, LSI (浅语义标号，有时也称LSA)](http://en.wikipedia.org/wiki/Latent_semantic_indexing)将文档从词袋或(更可取的)Tfidf权重空间转换为一个低维度的潜层空间。在上面的示例中我们使用了两个浅层，但是实际的语料库中，200-500的目标维度被认为是一个"黄金标准"。
```Python
>>> model = tfidfmodel.TfidfModel(bow_corpus, normalize=True)
```
LSI训练是唯一的，我们可以在任何时候继续训练，只需要提供更多的训练文档。这通过递增更新隐含模型来完成，这个过程被称为"在线训练"。因为这个特性，输入文档流甚至可以使无限的，只需要保持提供LSI新的文档，同时只读地使用这个计算转换的模型。
```Python
>>> model.add_documents(another_tfidf_corpus) # now LSI has been trained on tfidf_corpus + another_tfidf_corpus
>>> lsi_vec = model[tfidf_vec] # convert some new document into the LSI space, without affecting the model
>>> ...
>>> model.add_documents(more_documents) # tfidf_corpus + another_tfidf_corpus + more_documents
>>> lsi_vec = model[tfidf_vec]
>>> ...
```
查看`gensim.models.lsimodel`文档来获取使得LSI在无穷的输入流中渐进忘记旧的观测值的细节。如果想更进一步，也有一些参数你可以用来调节以改变LSI算法的速度或内存空间或数字精度。
+ [Random Projections, RP(随机映射)](http://www.cis.hut.fi/ella/publications/randproj_kdd.pdf)主要目的是减少向量空间的维度。这是一个非常高效的(CPU和内存)方法，通过扔一些随机数来近似文档间的Tfidf距离。推荐的目标维度基于数据集在成百上千之间。
```Python
>>> model = rpmodel.RpModel(tfidf_corpus, num_topics=500)
```
+ [Latent Dirichlet Allocation, LDA](http://en.wikipedia.org/wiki/Latent_Dirichlet_allocation)是另一种将词袋计数向量转换为低纬度主题空间的方法。LDA是LSA(也称多项分布PCA)的概率扩展，所以LDA的主题能够被解释为单词上的概率分布。这些分布，像LSA那样，通过训练语料库来自动推断。文档返过来解释这些主题的混合情况。
```Python
>>> model = ldamodel.LdaModel(bow_corpus, id2word=dictionary, num_topics=100)
```
gensim使用一个在线LDA参数评价的快速实现，可以在分布式集群上运行。

+ [Hierarchical Dirichlet Process, HDP](http://jmlr.csail.mit.edu/proceedings/papers/v15/wang11a/wang11a.pdf)是一个非参数的贝叶斯方法(表示请求主题的缺省数目)：
```Python
>>> model = hdpmodel.HdpModel(bow_corpus, id2word=dictionary)
```
gensim使用一个快速的在线实现。HDP模型是新添加如gensim的，在一些边界上存在问题，需要注意。

增加新的VSM变换(比如不同权重模式)十分简单，查看[API文档](http://radimrehurek.com/gensim/apiref.html)获得更多的细节。

值得再提一下的是，存在递增的不需要一次加载所有训练语料库的实现。注意内存的使用，是十分重要的。

## 相似度查询
相似度查询指文档间的相似度，或者一个特定文档与一系列其它文档的集合的相似度。

为了演示在gensim中如何完成，我们考虑之前的示例。
```Python
>>> from gensim import corpora, models, similarities
>>> dictionary = corpora.Dictionary.load('/tmp/deerwester.dict')
>>> corpus = corpora.MmCorpus('/tmp/deerwester.mm')
>>> print(corpus)
MmCorpus(9 documents, 12 features, 28 non-zero entries)
```
接下来定义一个二维的LSI空间。
```Python
>>> lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=2)
```

现在假定一个用户输入了查询词`Human computer interaciton`。我们应该能够讲九个语料库文档根据相关性进行排序。与现代搜索引擎不同，这里我们把重心放在单个概率相似性上——也即单词文本的明显的寓意相关性。不考虑超链接、随机游走、只考虑语义扩展。
```Python
>>> doc = "Human computer interaction"
>>> vec_bow = dictionary.doc2bow(doc.lower().split())
>>> vec_lsi = lsi[vec_bow] # convert the query to LSI space
>>> print(vec_lsi)
[(0, -0.461821), (1, 0.070028)]
```

另外，我们会考虑[cosine similarity](http://en.wikipedia.org/wiki/Cosine_similarity)来决定两个向量的相似度。

### 初始化查询结构
比较之前，我们需要输入所有用来比较的文档。这里有九个文档，用来训练LSI，转换为二维的LSD空间。不过，这个是可以渐进增加的，我们可以一起索引其它的语料库。
```Python
>>> index = similarities.MatrixSimilarity(lsi[corpus]) # 转换语料库到LSI空间并索引它
```

> 警告：类`similarities.MatrixSimilarity`只适合于所有的向量都在内存中。内存过少可以使用`similarities.Similarity`类。这个类使用固定的内存来操作，通过分片来实现。在内部它使用`similarities.MatrixSimilarity`和`similarities.SparseMatrixSimilarity`两个类，所以很快，尽管看起来更复杂些。

索引持久化通过标准的`save()`和`load()`函数来实现：
```Python
>>> index.save('/tmp/deerwester.index')
>>> index = similarities.MatrixSimilarity.load('/tmp/deerwester.index')
```

### 执行查询
获得查询文档的相似度:
```Python
>>> sims = index[vec_lsi] # perform a similarity query against the corpus
>>> print(list(enumerate(sims))) # print (document_number, document_similarity) 2-tuples
[(0, 0.99809301), (1, 0.93748635), (2, 0.99844527), (3, 0.9865886), (4, 0.90755945),
(5, -0.12416792), (6, -0.1063926), (7, -0.098794639), (8, 0.05004178)]
```

Cosine测量返回(-1,1)之间的相似度。

使用Python的标准函数，我们可以对相似度进行排序：
```Python
>>> sims = sorted(enumerate(sims), key=lambda item: -item[1])
>>> print(sims)   # print sorted (document number, similarity score) 2-tuples
[(2, 0.99844527), # The EPS user interface management system
(0, 0.99809301),  # Human machine interface for lab abc computer applications
(3, 0.9865886),   # System and human system engineering testing of EPS
(1, 0.93748635),  # A survey of user opinion of computer system response time
(4, 0.90755945),  # Relation of user perceived response time to error measurement
(8, 0.050041795), # Graph minors A survey
(7, -0.098794639),# Graph minors IV Widths of trees and well quasi ordering
(6, -0.1063926),  # The intersection graph of paths in trees
(5, -0.12416792)] # The generation of random binary unordered trees
```

需要注意的是文档2和4不可能会在标准布尔全文搜索中出现，因为它们与查询词没有任何共同词。然而，在应用了LSI后，我们能够查看到这两个都返回了较高的相似度，与我们的查询有很高的相关性。事实上，这个语义泛化正式我们首先应用变换和做主题建模的原因。

### 接下来是什么
祝贺，已经完成了辅导入门内容。后面可以查看API及Wikipedia实验或者查看gensim中的分布式计算内容。

Gensim是一个相当成熟的包，被很多人和公司使用，在生产环境下可以进行原型开发。但并不意味着它是足够完美的：

- 存在一些需要更高效实现的地方(比如用C实现)，或者并行的实现。
- 新的算法层出不穷。


[TOC]

