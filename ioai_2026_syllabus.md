IOAI 2026 Syllabus

International Olympiad in Artificial Intelligence (IOAI)

Introduction

The International Olympiad in Artificial Intelligence (IOAI) is a premier global competition for high
school students, aiming to cultivate both a strong theoretical foundation and hands-on expertise in Arti-
ficial Intelligence. This syllabus outlines the topics contestants should master to excel in the competition.
Each year, the IOAI International Scientific Committee (ISC) updates the official syllabus to reflect the
latest research findings and educational priorities.

Topic Classifications

The topics are categorized into three distinct sections, indicating the level and nature of knowledge
contestants need:

1. Theory (How it works): Contestants should understand core concepts and theoretical underpin-
nings—the “why” behind AI. This may involve studying textbooks, courses, and other resources
to delve into the mechanics that power AI algorithms. Breadth should be prioritized over depth in
covering all relevant topics.

2. Practice (What it does, when to use it, and how to implement it): Contestants should
develop practical skills necessary to implement AI methods in code. This includes knowing how
to use library functions effectively, call the method on a particular data, and interpret outputs.
Example: While a contestant need not fully dissect the internal workings of the Adam optimizer,
they should be able to decide when and how to employ it.

3. Both: Certain topics require knowledge of both theoretical principles and practical application.

This structured approach ensures that contestants acquire the right balance of conceptual insight and
hands-on proficiency across the diverse array of AI topics. Topics not listed are considered excluded from
the syllabus. Questions can be directed to isc@ioai-official.org.

1

1 Foundational Skills & Classical Machine Learning

Topic

Subtopic

Category

Programming Fundamentals

Supervised Learning

Unsupervised Learning

Python Basics (Loops, Functions, etc.)
NumPy and Pandas for Data Handling
Matplotlib and Seaborn for Visualization
Scikit-learn for ML
PyTorch Basics
Tensor (Multi-dimensional Array) Manipulation
Training Models on CPU and GPU

Linear Regression
Logistic Regression
L1 & L2 Regularization
K-Nearest Neighbors (K-NN)
Decision Trees
Model Ensembles (Gradient Boosting, Bagging,
Random Forest)
Support Vector Machines (SVM)

K-Means Clustering
Principal Component Analysis (PCA)
t-SNE, UMAP
DBSCAN, Hierarchical & Spectral Clustering

Practice
Practice
Practice
Practice
Practice
Practice
Practice

Both
Both
Both
Both
Both
Practice

Both

Both
Both
Practice
Practice

Data Science Fundamentals Model Evaluation Metrics (Accuracy, Precision,

Both

Recall, F1-Score, etc.)
Underfitting, Overfitting
Hyperparameter Tuning
Cross-Validation
Confusion Matrix and ROC Curves
Feature Engineering *
Data Processing **

Theory
Practice
Practice
Both
Practice
Practice

* Feature Engineering involves transforming raw, potentially high-dimensional data, categorical data,
time series, or ragged data into a compact set of informative features. Techniques involve sliding windows,
pooling operations, one-hot encoding, statistical moment-based features (average, standard deviation),
PCA and neural-network-based embeddings.
** Data Processing concerns the handling of missing data and irregular data, including in sequence mod-
eling settings. Techniques involve basic imputation strategies (mean/median/forward-fill for sequences)
and padding for variable-length sequences. Covered here are also normalization and standardization
techniques, train/validation/test splitting strategies, basic data augmentation (flipping, cropping, noise
addition), tokenization and vocabulary building for text and audio and patching for images.

2 Neural Networks & Deep Learning

Topic

Neural Networks

Deep Learning

Subtopic

Category

Perceptron Basics
Gradient Descent
Backpropagation
Activation Functions (ReLU, Sigmoid, Tanh)
Loss Functions (MSE, MAE, Cross Entropy, etc.)

Multi-Layer Perceptrons (MLP)
Data Embeddings (text, image, audio)
Pooling Techniques (Max, Average)

Both
Both
Both
Both
Both

Both
Both
Both

2

Both
Attention Mechanism
Transformers (theory needed only for text and image) Both
Autoencoders
SGD, Mini-Batch Gradient Descent
Momentum Methods (Adam, AdamW)
Convergence and Learning Rates
Regularization: Dropout, Early Stopping, Weight De-
cay
Weight Initialization
Batch Normalization
Model Finetuning (full and parameter-efficient)

Practice
Both
Practice
Practice
Practice

Practice
Practice
Practice

3 Computer Vision

Topic

Fundamentals

Subtopic

Convolutional Layers
Image Classification
Object Detection (YOLO, SSD, DERT)
Image Segmentation (U-Net)
Pre-trained Vision Encoders (e.g. ResNet)
Image Augmentation
Generating Images with GANs
Self-Supervised Learning for Vision
Vision-text encoders (e.g. CLIP)
Diffusion Models

4 Natural Language Processing & Audio

Topic

NLP

Subtopic

Text Classification
Pre-trained Text Encoders (e.g. BERT)
Language Modeling
Encoder-Decoder Models (e.g.
tion or Vision-Language Modeling)
Pre-trained Language Models (open-source and API-
based ones)

for Machine Transla-

Audio Processing

Pre-trained Audio Encoders: HuBERT
Audio Models: Qwen-Audio, Whisper, Voxtral

Category

Both
Practice
Practice
Practice
Practice
Practice
Practice
Practice
Practice
Practice

Category

Practice
Both
Both
Practice

Practice

Practice
Practice

NB: The data can be text, tabular, image, audio, video, and time-series, and should be processed with
the methods above.

3

