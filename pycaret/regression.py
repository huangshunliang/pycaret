# Module: Regression
# Author: Moez Ali <moez.ali@queensu.ca>
# License: MIT
# Release: PyCaret 2.1
# Last modified : 14/08/2020

def setup(data, 
          target, 
          train_size = 0.7,
          sampling = True,
          sample_estimator = None,
          categorical_features = None,
          categorical_imputation = 'constant',
          ordinal_features = None,
          high_cardinality_features = None, 
          high_cardinality_method = 'frequency', 
          numeric_features = None,
          numeric_imputation = 'mean',
          date_features = None,
          ignore_features = None,
          normalize = False,
          normalize_method = 'zscore',
          transformation = False,
          transformation_method = 'yeo-johnson',
          handle_unknown_categorical = True,              
          unknown_categorical_method = 'least_frequent',
          pca = False,
          pca_method = 'linear',
          pca_components = None, 
          ignore_low_variance = False, 
          combine_rare_levels = False,
          rare_level_threshold = 0.10,
          bin_numeric_features = None, 
          remove_outliers = False,
          outliers_threshold = 0.05,
          remove_multicollinearity = False,
          multicollinearity_threshold = 0.9,
          remove_perfect_collinearity = False, #added in pycaret==2.0.0
          create_clusters = False,
          cluster_iter = 20,
          polynomial_features = False,           
          polynomial_degree = 2,
          trigonometry_features = False,
          polynomial_threshold = 0.1,
          group_features = None,
          group_names = None,
          feature_selection = False,
          feature_selection_threshold = 0.8,
          feature_interaction = False,
          feature_ratio = False,
          interaction_threshold = 0.01,              
          transform_target = False,
          transform_target_method = 'box-cox',
          data_split_shuffle = True, #added in pycaret==2.0.0
          folds_shuffle = False, #added in pycaret==2.0.0
          n_jobs = -1, #added in pycaret==2.0.0
          use_gpu = False, #added in pycaret==2.1
          html = True, #added in pycaret==2.0.0
          session_id = None,
          log_experiment = False, #added in pycaret==2.0.0
          experiment_name = None, #added in pycaret==2.0.0
          log_plots = False, #added in pycaret==2.0.0
          log_profile = False, #added in pycaret==2.0.0
          log_data = False, #added in pycaret==2.0.0
          silent = False,
          verbose = True, #added in pycaret==2.0.0
          profile = False):
    
    """
    This function initializes the environment in pycaret and creates the transformation
    pipeline to prepare the data for modeling and deployment. setup() must called before
    executing any other function in pycaret. It takes two mandatory parameters:
    dataframe {array-like, sparse matrix} and name of the target column. 
    
    All other parameters are optional.

    Example
    -------
    >>> from pycaret.datasets import get_data
    >>> boston = get_data('boston')
    
    >>> experiment_name = setup(data = boston,  target = 'medv')

    'boston' is a pandas.DataFrame and 'medv' is the name of target column.

    Parameters
    ----------
    data : pandas.DataFrame
        Shape (n_samples, n_features) where n_samples is the number of samples and n_features is the number of features.

    target: string
        Name of target column to be passed in as string. 
    
    train_size: float, default = 0.7
        Size of the training set. By default, 70% of the data will be used for training 
        and validation. The remaining data will be used for test / hold-out set.

    sampling: bool, default = True
        When the sample size exceeds 25,000 samples, pycaret will build a base estimator
        at various sample sizes from the original dataset. This will return a performance 
        plot of R2 values at various sample levels, that will assist in deciding the 
        preferred sample size for modeling.  The desired sample size must then be entered 
        for training and validation in the  pycaret environment. When sample_size entered 
        is less than 1, the remaining dataset (1 - sample) is used for fitting the model 
        only when finalize_model() is called.
    
    sample_estimator: object, default = None
        If None, Linear Regression is used by default.
    
    categorical_features: string, default = None
        If the inferred data types are not correct, categorical_features can be used to
        overwrite the inferred type. If when running setup the type of 'column1' is
        inferred as numeric instead of categorical, then this parameter can be used 
        to overwrite the type by passing categorical_features = ['column1'].
    
    categorical_imputation: string, default = 'constant'
        If missing values are found in categorical features, they will be imputed with
        a constant 'not_available' value. The other available option is 'mode' which 
        imputes the missing value using most frequent value in the training dataset. 
    
    ordinal_features: dictionary, default = None
        When the data contains ordinal features, they must be encoded differently using 
        the ordinal_features param. If the data has a categorical variable with values
        of 'low', 'medium', 'high' and it is known that low < medium < high, then it can 
        be passed as ordinal_features = { 'column_name' : ['low', 'medium', 'high'] }. 
        The list sequence must be in increasing order from lowest to highest.
    
    high_cardinality_features: string, default = None
        When the data containts features with high cardinality, they can be compressed
        into fewer levels by passing them as a list of column names with high cardinality.
        Features are compressed using method defined in high_cardinality_method param.
    
    high_cardinality_method: string, default = 'frequency'
        When method set to 'frequency' it will replace the original value of feature
        with the frequency distribution and convert the feature into numeric. Other
        available method is 'clustering' which performs the clustering on statistical
        attribute of data and replaces the original value of feature with cluster label.
        The number of clusters is determined using a combination of Calinski-Harabasz and 
        Silhouette criterion. 
    
    numeric_features: string, default = None
        If the inferred data types are not correct, numeric_features can be used to
        overwrite the inferred type. If when running setup the type of 'column1' is 
        inferred as a categorical instead of numeric, then this parameter can be used 
        to overwrite by passing numeric_features = ['column1'].    

    numeric_imputation: string, default = 'mean'
        If missing values are found in numeric features, they will be imputed with the 
        mean value of the feature. The other available option is 'median' which imputes 
        the value using the median value in the training dataset. 
    
    date_features: string, default = None
        If the data has a DateTime column that is not automatically detected when running
        setup, this parameter can be used by passing date_features = 'date_column_name'. 
        It can work with multiple date columns. Date columns are not used in modeling. 
        Instead, feature extraction is performed and date columns are dropped from the 
        dataset. If the date column includes a time stamp, features related to time will 
        also be extracted.
    
    ignore_features: string, default = None
        If any feature should be ignored for modeling, it can be passed to the param
        ignore_features. The ID and DateTime columns when inferred, are automatically 
        set to ignore for modeling. 
    
    normalize: bool, default = False
        When set to True, the feature space is transformed using the normalized_method
        param. Generally, linear algorithms perform better with normalized data however, 
        the results may vary and it is advised to run multiple experiments to evaluate
        the benefit of normalization.
    
    normalize_method: string, default = 'zscore'
        Defines the method to be used for normalization. By default, normalize method
        is set to 'zscore'. The standard zscore is calculated as z = (x - u) / s. The
        other available options are:
        
        'minmax'    : scales and translates each feature individually such that it is in 
                    the range of 0 - 1.
        
        'maxabs'    : scales and translates each feature individually such that the maximal 
                    absolute value of each feature will be 1.0. It does not shift/center 
                    the data, and thus does not destroy any sparsity.
        
        'robust'    : scales and translates each feature according to the Interquartile range.
                    When the dataset contains outliers, robust scaler often gives better
                    results.
    
    transformation: bool, default = False
        When set to True, a power transformation is applied to make the data more normal /
        Gaussian-like. This is useful for modeling issues related to heteroscedasticity or 
        other situations where normality is desired. The optimal parameter for stabilizing 
        variance and minimizing skewness is estimated through maximum likelihood.
    
    transformation_method: string, default = 'yeo-johnson'
        Defines the method for transformation. By default, the transformation method is set
        to 'yeo-johnson'. The other available option is 'quantile' transformation. Both 
        the transformation transforms the feature set to follow a Gaussian-like or normal
        distribution. Note that the quantile transformer is non-linear and may distort linear 
        correlations between variables measured at the same scale.
    
    handle_unknown_categorical: bool, default = True
        When set to True, unknown categorical levels in new / unseen data are replaced by
        the most or least frequent level as learned in the training data. The method is 
        defined under the unknown_categorical_method param.
    
    unknown_categorical_method: string, default = 'least_frequent'
        Method used to replace unknown categorical levels in unseen data. Method can be
        set to 'least_frequent' or 'most_frequent'.
    
    pca: bool, default = False
        When set to True, dimensionality reduction is applied to project the data into 
        a lower dimensional space using the method defined in pca_method param. In 
        supervised learning pca is generally performed when dealing with high feature
        space and memory is a constraint. Note that not all datasets can be decomposed
        efficiently using a linear PCA technique and that applying PCA may result in loss 
        of information. As such, it is advised to run multiple experiments with different 
        pca_methods to evaluate the impact. 

    pca_method: string, default = 'linear'
        The 'linear' method performs Linear dimensionality reduction using Singular Value 
        Decomposition. The other available options are:
        
        kernel      : dimensionality reduction through the use of RVF kernel.  
        
        incremental : replacement for 'linear' pca when the dataset to be decomposed is 
                    too large to fit in memory

    pca_components: int/float, default = 0.99
        Number of components to keep. if pca_components is a float, it is treated as a 
        target percentage for information retention. When pca_components is an integer
        it is treated as the number of features to be kept. pca_components must be strictly
        less than the original number of features in the dataset.
    
    ignore_low_variance: bool, default = False
        When set to True, all categorical features with statistically insignificant variances 
        are removed from the dataset. The variance is calculated using the ratio of unique 
        values to the number of samples, and the ratio of the most common value to the 
        frequency of the second most common value.
    
    combine_rare_levels: bool, default = False
        When set to True, all levels in categorical features below the threshold defined 
        in rare_level_threshold param are combined together as a single level. There must be 
        atleast two levels under the threshold for this to take effect. rare_level_threshold
        represents the percentile distribution of level frequency. Generally, this technique 
        is applied to limit a sparse matrix caused by high numbers of levels in categorical 
        features. 
    
    rare_level_threshold: float, default = 0.1
        Percentile distribution below which rare categories are combined. Only comes into
        effect when combine_rare_levels is set to True.
    
    bin_numeric_features: list, default = None
        When a list of numeric features is passed they are transformed into categorical
        features using KMeans, where values in each bin have the same nearest center of a 
        1D k-means cluster. The number of clusters are determined based on the 'sturges' 
        method. It is only optimal for gaussian data and underestimates the number of bins 
        for large non-gaussian datasets.
    
    remove_outliers: bool, default = False
        When set to True, outliers from the training data are removed using PCA linear
        dimensionality reduction using the Singular Value Decomposition technique.
    
    outliers_threshold: float, default = 0.05
        The percentage / proportion of outliers in the dataset can be defined using
        the outliers_threshold param. By default, 0.05 is used which means 0.025 of the 
        values on each side of the distribution's tail are dropped from training data.
    
    remove_multicollinearity: bool, default = False
        When set to True, the variables with inter-correlations higher than the threshold
        defined under the multicollinearity_threshold param are dropped. When two features
        are highly correlated with each other, the feature that is less correlated with 
        the target variable is dropped. 
    
    multicollinearity_threshold: float, default = 0.9
        Threshold used for dropping the correlated features. Only comes into effect when 
        remove_multicollinearity is set to True.
    
    remove_perfect_collinearity: bool, default = False
        When set to True, perfect collinearity (features with correlation = 1) is removed
        from the dataset, When two features are 100% correlated, one of it is randomly 
        dropped from the dataset.

    create_clusters: bool, default = False
        When set to True, an additional feature is created where each instance is assigned
        to a cluster. The number of clusters is determined using a combination of 
        Calinski-Harabasz and Silhouette criterion. 
    
    cluster_iter: int, default = 20
        Number of iterations used to create a cluster. Each iteration represents cluster 
        size. Only comes into effect when create_clusters param is set to True.
    
    polynomial_features: bool, default = False
        When set to True, new features are created based on all polynomial combinations 
        that exist within the numeric features in a dataset to the degree defined in 
        polynomial_degree param. 
    
    polynomial_degree: int, default = 2
        Degree of polynomial features. For example, if an input sample is two dimensional 
        and of the form [a, b], the polynomial features with degree = 2 are: 
        [1, a, b, a^2, ab, b^2].
    
    trigonometry_features: bool, default = False
        When set to True, new features are created based on all trigonometric combinations 
        that exist within the numeric features in a dataset to the degree defined in the
        polynomial_degree param.
    
    polynomial_threshold: float, default = 0.1
        This is used to compress a sparse matrix of polynomial and trigonometric features.
        Polynomial and trigonometric features whose feature importance based on the 
        combination of Random Forest, AdaBoost and Linear correlation falls within the 
        percentile of the defined threshold are kept in the dataset. Remaining features 
        are dropped before further processing.
    
    group_features: list or list of list, default = None
        When a dataset contains features that have related characteristics, the group_features
        param can be used for statistical feature extraction. For example, if a dataset has 
        numeric features that are related with each other (i.e 'Col1', 'Col2', 'Col3'), a list 
        containing the column names can be passed under group_features to extract statistical 
        information such as the mean, median, mode and standard deviation.
    
    group_names: list, default = None
        When group_features is passed, a name of the group can be passed into the group_names 
        param as a list containing strings. The length of a group_names list must equal to the 
        length  of group_features. When the length doesn't match or the name is not passed, new 
        features are sequentially named such as group_1, group_2 etc.
    
    feature_selection: bool, default = False
        When set to True, a subset of features are selected using a combination of various
        permutation importance techniques including Random Forest, Adaboost and Linear 
        correlation with target variable. The size of the subset is dependent on the 
        feature_selection_param. Generally, this is used to constrain the feature space 
        in order to improve efficiency in modeling. When polynomial_features and 
        feature_interaction  are used, it is highly recommended to define the 
        feature_selection_threshold param with a lower value.

    feature_selection_threshold: float, default = 0.8
        Threshold used for feature selection (including newly created polynomial features).
        A higher value will result in a higher feature space. It is recommended to do multiple
        trials with different values of feature_selection_threshold specially in cases where 
        polynomial_features and feature_interaction are used. Setting a very low value may be 
        efficient but could result in under-fitting.
    
    feature_interaction: bool, default = False 
        When set to True, it will create new features by interacting (a * b) for all numeric 
        variables in the dataset including polynomial and trigonometric features (if created). 
        This feature is not scalable and may not work as expected on datasets with large 
        feature space.
    
    feature_ratio: bool, default = False
        When set to True, it will create new features by calculating the ratios (a / b) of all 
        numeric variables in the dataset. This feature is not scalable and may not work as 
        expected on datasets with large feature space.
    
    interaction_threshold: bool, default = 0.01
        Similar to polynomial_threshold, It is used to compress a sparse matrix of newly 
        created features through interaction. Features whose importance based on the 
        combination  of  Random Forest, AdaBoost and Linear correlation falls within the 
        percentile of the  defined threshold are kept in the dataset. Remaining features 
        are dropped before further processing.
    
    transform_target: bool, default = False
        When set to True, target variable is transformed using the method defined in
        transform_target_method param. Target transformation is applied separately from 
        feature transformations. 
    
    transform_target_method: string, default = 'box-cox'
        'Box-cox' and 'yeo-johnson' methods are supported. Box-Cox requires input data to 
        be strictly positive, while Yeo-Johnson supports both positive or negative data.
        When transform_target_method is 'box-cox' and target variable contains negative
        values, method is internally forced to 'yeo-johnson' to avoid exceptions.

    data_split_shuffle: bool, default = True
        If set to False, prevents shuffling of rows when splitting data.

    folds_shuffle: bool, default = True
        If set to False, prevents shuffling of rows when using cross validation.

    n_jobs: int, default = -1
        The number of jobs to run in parallel (for functions that supports parallel 
        processing) -1 means using all processors. To run all functions on single processor 
        set n_jobs to None.

    use_gpu: bool, default = False
        If set to True, algorithms that supports gpu are trained using gpu.

    html: bool, default = True
        If set to False, prevents runtime display of monitor. This must be set to False
        when using environment that doesnt support HTML.
    
    session_id: int, default = None
        If None, a random seed is generated and returned in the Information grid. The 
        unique number is then distributed as a seed in all functions used during the 
        experiment. This can be used for later reproducibility of the entire experiment.

    log_experiment: bool, default = False
        When set to True, all metrics and parameters are logged on MLFlow server.

    experiment_name: str, default = None
        Name of experiment for logging. When set to None, 'reg' is by default used as 
        alias for the experiment name.

    log_plots: bool, default = False
        When set to True, specific plots are logged in MLflow as a png file. By default,
        it is set to False. 

    log_profile: bool, default = False
        When set to True, data profile is also logged on MLflow as a html file. By default,
        it is set to False. 

    log_data: bool, default = False
        When set to True, train and test dataset are logged as csv. 
    
    silent: bool, default = False
        When set to True, confirmation of data types is not required. All preprocessing will 
        be performed assuming automatically inferred data types. Not recommended for direct use 
        except for established pipelines.

    verbose: Boolean, default = True
        Information grid is not printed when verbose is set to False.

    profile: bool, default = False
        If set to true, a data profile for Exploratory Data Analysis will be displayed 
        in an interactive HTML report. 
    
    Returns
    -------
    info_grid
        Information grid is printed.

    environment
        This function returns various outputs that are stored in variable
        as tuple. They are used by other functions in pycaret.
      
    """
    
    #exception checking   
    import sys
    
    from pycaret.utils import __version__
    ver = __version__()

    import logging

    # create logger
    global logger

    logger = logging.getLogger('logs')
    logger.setLevel(logging.DEBUG)
    
    # create console handler and set level to debug

    if logger.hasHandlers():
        logger.handlers.clear()
        
    ch = logging.FileHandler('logs.log')
    ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)

    logger.info("PyCaret Regression Module")
    logger.info('version ' + str(ver))
    logger.info("Initializing setup()")

    #generate USI for mlflow tracking
    import secrets
    global USI
    USI = secrets.token_hex(nbytes=2)
    logger.info('USI: ' + str(USI))

    logger.info("""setup(data={}, target={}, train_size={}, sampling={}, sample_estimator={}, categorical_features={}, categorical_imputation={}, ordinal_features={},
                    high_cardinality_features={}, high_cardinality_method={}, numeric_features={}, numeric_imputation={}, date_features={}, ignore_features={}, normalize={},
                    normalize_method={}, transformation={}, transformation_method={}, handle_unknown_categorical={}, unknown_categorical_method={}, pca={}, pca_method={},
                    pca_components={}, ignore_low_variance={}, combine_rare_levels={}, rare_level_threshold={}, bin_numeric_features={}, remove_outliers={}, outliers_threshold={},
                    remove_multicollinearity={}, multicollinearity_threshold={}, remove_perfect_collinearity={}, create_clusters={}, cluster_iter={},
                    polynomial_features={}, polynomial_degree={}, trigonometry_features={}, polynomial_threshold={}, group_features={},
                    group_names={}, feature_selection={}, feature_selection_threshold={}, feature_interaction={}, feature_ratio={}, interaction_threshold={}, transform_target={},
                    transform_target_method={}, data_split_shuffle={}, folds_shuffle={}, n_jobs={}, html={}, session_id={}, log_experiment={},
                    experiment_name={}, log_plots={}, log_profile={}, log_data={}, silent={}, verbose={}, profile={})""".format(\
            str(data.shape), str(target), str(train_size), str(sampling), str(sample_estimator), str(categorical_features), str(categorical_imputation), str(ordinal_features),\
            str(high_cardinality_features), str(high_cardinality_method), str(numeric_features), str(numeric_imputation), str(date_features), str(ignore_features),\
            str(normalize), str(normalize_method), str(transformation), str(transformation_method), str(handle_unknown_categorical), str(unknown_categorical_method), str(pca),\
            str(pca_method), str(pca_components), str(ignore_low_variance), str(combine_rare_levels), str(rare_level_threshold), str(bin_numeric_features), str(remove_outliers),\
            str(outliers_threshold), str(remove_multicollinearity), str(multicollinearity_threshold), str(remove_perfect_collinearity), str(create_clusters), str(cluster_iter),\
            str(polynomial_features), str(polynomial_degree), str(trigonometry_features), str(polynomial_threshold), str(group_features), str(group_names),\
            str(feature_selection), str(feature_selection_threshold), str(feature_interaction), str(feature_ratio), str(interaction_threshold), str(transform_target),\
            str(transform_target_method), str(data_split_shuffle), str(folds_shuffle), str(n_jobs), str(html), str(session_id),\
            str(log_experiment), str(experiment_name), str(log_plots), str(log_profile), str(log_data), str(silent), str(verbose), str(profile)))

    #logging environment and libraries
    logger.info("Checking environment")
    
    from platform import python_version, platform, python_build, machine

    try:
        logger.info("python_version: " + str(python_version()))
    except:
        logger.warning("cannot find platform.python_version")

    try:
        logger.info("python_build: " + str(python_build()))
    except:
        logger.warning("cannot find platform.python_build")

    try:
        logger.info("machine: " + str(machine()))
    except:
        logger.warning("cannot find platform.machine")

    try:
        logger.info("platform: " + str(platform()))
    except:
        logger.warning("cannot find platform.platform")

    try:
        import psutil
        logger.info("Memory: " + str(psutil.virtual_memory()))
        logger.info("Physical Core: " + str(psutil.cpu_count(logical=False)))
        logger.info("Logical Core: " + str(psutil.cpu_count(logical=True)))
    except:
        logger.warning("cannot find psutil installation. memory not traceable. Install psutil using pip to enable memory logging. ")
    
    logger.info("Checking libraries")

    try:
        from pandas import __version__
        logger.info("pd==" + str(__version__))
    except:
        logger.warning("pandas not found")

    try:
        from numpy import __version__
        logger.info("numpy==" + str(__version__))
    except:
        logger.warning("numpy not found")

    try:
        from sklearn import __version__
        logger.info("sklearn==" + str(__version__))
    except:
        logger.warning("sklearn not found")

    try:
        from xgboost import __version__
        logger.info("xgboost==" + str(__version__))
    except:
        logger.warning("xgboost not found")

    try:
        from lightgbm import __version__
        logger.info("lightgbm==" + str(__version__))
    except:
        logger.warning("lightgbm not found")

    try:
        from catboost import __version__
        logger.info("catboost==" + str(__version__))
    except:
        logger.warning("catboost not found")

    try:
        from mlflow.version import VERSION
        import warnings
        warnings.filterwarnings('ignore') 
        logger.info("mlflow==" + str(VERSION))
    except:
        logger.warning("mlflow not found")

    #run_time
    import datetime, time
    runtime_start = time.time()

    logger.info("Checking Exceptions")

    #checking train size parameter
    if type(train_size) is not float:
        sys.exit('(Type Error): train_size parameter only accepts float value.')
    
    #checking sampling parameter
    if type(sampling) is not bool:
        sys.exit('(Type Error): sampling parameter only accepts True or False.')
        
    #checking sampling parameter
    if target not in data.columns:
        sys.exit('(Value Error): Target parameter doesnt exist in the data provided.')   

    #checking session_id
    if session_id is not None:
        if type(session_id) is not int:
            sys.exit('(Type Error): session_id parameter must be an integer.')   
    
    #checking sampling parameter
    if type(profile) is not bool:
        sys.exit('(Type Error): profile parameter only accepts True or False.')
      
    #checking normalize parameter
    if type(normalize) is not bool:
        sys.exit('(Type Error): normalize parameter only accepts True or False.')
        
    #checking transformation parameter
    if type(transformation) is not bool:
        sys.exit('(Type Error): transformation parameter only accepts True or False.')
        
    #checking categorical imputation
    allowed_categorical_imputation = ['constant', 'mode']
    if categorical_imputation not in allowed_categorical_imputation:
        sys.exit("(Value Error): categorical_imputation param only accepts 'constant' or 'mode' ")
    
    #ordinal_features
    if ordinal_features is not None:
        if type(ordinal_features) is not dict:
            sys.exit("(Type Error): ordinal_features must be of type dictionary with column name as key and ordered values as list. ")
    
    #ordinal features check
    if ordinal_features is not None:
        data_cols = data.columns
        data_cols = data_cols.drop(target)
        ord_keys = ordinal_features.keys()
        
        for i in ord_keys:
            if i not in data_cols:
                sys.exit("(Value Error) Column name passed as a key in ordinal_features param doesnt exist. ")
                
        for k in ord_keys:
            if data[k].nunique() != len(ordinal_features.get(k)):
                sys.exit("(Value Error) Levels passed in ordinal_features param doesnt match with levels in data. ")

        for i in ord_keys:
            value_in_keys = ordinal_features.get(i)
            value_in_data = list(data[i].unique().astype(str))
            for j in value_in_keys:
                if j not in value_in_data:
                    text =  "Column name '" + str(i) + "' doesnt contain any level named '" + str(j) + "'."
                    sys.exit(text)
           
    #high_cardinality_features
    if high_cardinality_features is not None:
        if type(high_cardinality_features) is not list:
            sys.exit("(Type Error): high_cardinality_features param only accepts name of columns as a list. ")
        
    if high_cardinality_features is not None:
        data_cols = data.columns
        data_cols = data_cols.drop(target)
        for i in high_cardinality_features:
            if i not in data_cols:
                sys.exit("(Value Error): Column type forced is either target column or doesn't exist in the dataset.")
                
    #checking numeric imputation
    allowed_numeric_imputation = ['mean', 'median']
    if numeric_imputation not in allowed_numeric_imputation:
        sys.exit("(Value Error): numeric_imputation param only accepts 'mean' or 'median' ")
        
    #checking normalize method
    allowed_normalize_method = ['zscore', 'minmax', 'maxabs', 'robust']
    if normalize_method not in allowed_normalize_method:
        sys.exit("(Value Error): normalize_method param only accepts 'zscore', 'minxmax', 'maxabs' or 'robust'. ")      
    
    #checking transformation method
    allowed_transformation_method = ['yeo-johnson', 'quantile']
    if transformation_method not in allowed_transformation_method:
        sys.exit("(Value Error): transformation_method param only accepts 'yeo-johnson' or 'quantile' ")        
    
    #handle unknown categorical
    if type(handle_unknown_categorical) is not bool:
        sys.exit('(Type Error): handle_unknown_categorical parameter only accepts True or False.')
        
    #unknown categorical method
    unknown_categorical_method_available = ['least_frequent', 'most_frequent']
    
    if unknown_categorical_method not in unknown_categorical_method_available:
        sys.exit("(Type Error): unknown_categorical_method only accepts 'least_frequent' or 'most_frequent'.")
    
    #check pca
    if type(pca) is not bool:
        sys.exit('(Type Error): PCA parameter only accepts True or False.')
        
    #pca method check
    allowed_pca_methods = ['linear', 'kernel', 'incremental',]
    if pca_method not in allowed_pca_methods:
        sys.exit("(Value Error): pca method param only accepts 'linear', 'kernel', or 'incremental'. ")    
    
    #pca components check
    if pca is True:
        if pca_method != 'linear':
            if pca_components is not None:
                if(type(pca_components)) is not int:
                    sys.exit("(Type Error): pca_components parameter must be integer when pca_method is not 'linear'. ")

    #pca components check 2
    if pca is True:
        if pca_method != 'linear':
            if pca_components is not None:
                if pca_components > len(data.columns)-1:
                    sys.exit("(Type Error): pca_components parameter cannot be greater than original features space.")                
 
    #pca components check 3
    if pca is True:
        if pca_method == 'linear':
            if pca_components is not None:
                if type(pca_components) is not float:
                    if pca_components > len(data.columns)-1: 
                        sys.exit("(Type Error): pca_components parameter cannot be greater than original features space or float between 0 - 1.")      
    
    #check ignore_low_variance
    if type(ignore_low_variance) is not bool:
        sys.exit('(Type Error): ignore_low_variance parameter only accepts True or False.')
        
    #check ignore_low_variance
    if type(combine_rare_levels) is not bool:
        sys.exit('(Type Error): combine_rare_levels parameter only accepts True or False.')
        
    #check rare_level_threshold
    if type(rare_level_threshold) is not float:
        sys.exit('(Type Error): rare_level_threshold must be a float between 0 and 1. ')
    
    #bin numeric features
    if bin_numeric_features is not None:
        all_cols = list(data.columns)
        all_cols.remove(target)
        
        for i in bin_numeric_features:
            if i not in all_cols:
                sys.exit("(Value Error): Column type forced is either target column or doesn't exist in the dataset.")
    
    #check transform_target
    if type(transform_target) is not bool:
        sys.exit('(Type Error): transform_target parameter only accepts True or False.')
        
    #transform_target_method
    allowed_transform_target_method = ['box-cox', 'yeo-johnson']
    if transform_target_method not in allowed_transform_target_method:
        sys.exit("(Value Error): transform_target_method param only accepts 'box-cox' or 'yeo-johnson'. ") 
    
    #remove_outliers
    if type(remove_outliers) is not bool:
        sys.exit('(Type Error): remove_outliers parameter only accepts True or False.')    
    
    #outliers_threshold
    if type(outliers_threshold) is not float:
        sys.exit('(Type Error): outliers_threshold must be a float between 0 and 1. ')   
        
    #remove_multicollinearity
    if type(remove_multicollinearity) is not bool:
        sys.exit('(Type Error): remove_multicollinearity parameter only accepts True or False.')
        
    #multicollinearity_threshold
    if type(multicollinearity_threshold) is not float:
        sys.exit('(Type Error): multicollinearity_threshold must be a float between 0 and 1. ')  
        
    #create_clusters
    if type(create_clusters) is not bool:
        sys.exit('(Type Error): create_clusters parameter only accepts True or False.')
        
    #cluster_iter
    if type(cluster_iter) is not int:
        sys.exit('(Type Error): cluster_iter must be a integer greater than 1. ') 
    
    #polynomial_features
    if type(polynomial_features) is not bool:
        sys.exit('(Type Error): polynomial_features only accepts True or False. ')   
    
    #polynomial_degree
    if type(polynomial_degree) is not int:
        sys.exit('(Type Error): polynomial_degree must be an integer. ')
        
    #polynomial_features
    if type(trigonometry_features) is not bool:
        sys.exit('(Type Error): trigonometry_features only accepts True or False. ')    
        
    #polynomial threshold
    if type(polynomial_threshold) is not float:
        sys.exit('(Type Error): polynomial_threshold must be a float between 0 and 1. ')      
        
    #group features
    if group_features is not None:
        if type(group_features) is not list:
            sys.exit('(Type Error): group_features must be of type list. ')     
    
    if group_names is not None:
        if type(group_names) is not list:
            sys.exit('(Type Error): group_names must be of type list. ')         
    
    #cannot drop target
    if ignore_features is not None:
        if target in ignore_features:
            sys.exit("(Value Error): cannot drop target column. ")  
                
    #feature_selection
    if type(feature_selection) is not bool:
        sys.exit('(Type Error): feature_selection only accepts True or False. ')   
        
    #feature_selection_threshold
    if type(feature_selection_threshold) is not float:
        sys.exit('(Type Error): feature_selection_threshold must be a float between 0 and 1. ')  
        
    #feature_interaction
    if type(feature_interaction) is not bool:
        sys.exit('(Type Error): feature_interaction only accepts True or False. ')  
        
    #feature_ratio
    if type(feature_ratio) is not bool:
        sys.exit('(Type Error): feature_ratio only accepts True or False. ')     
        
    #interaction_threshold
    if type(interaction_threshold) is not float:
        sys.exit('(Type Error): interaction_threshold must be a float between 0 and 1. ')      

    #cannot drop target
    if ignore_features is not None:
        if target in ignore_features:
            sys.exit("(Value Error): cannot drop target column. ")  
        
    #forced type check
    all_cols = list(data.columns)
    all_cols.remove(target)
    
    #categorical
    if categorical_features is not None:
        for i in categorical_features:
            if i not in all_cols:
                sys.exit("(Value Error): Column type forced is either target column or doesn't exist in the dataset.")
        
    #numeric
    if numeric_features is not None:
        for i in numeric_features:
            if i not in all_cols:
                sys.exit("(Value Error): Column type forced is either target column or doesn't exist in the dataset.")    
    
    #date features
    if date_features is not None:
        for i in date_features:
            if i not in all_cols:
                sys.exit("(Value Error): Column type forced is either target column or doesn't exist in the dataset.")      
    
    #drop features
    if ignore_features is not None:
        for i in ignore_features:
            if i not in all_cols:
                sys.exit("(Value Error): Feature ignored is either target column or doesn't exist in the dataset.") 
     
    #silent
    if type(silent) is not bool:
        sys.exit("(Type Error): silent parameter only accepts True or False. ")

    #remove_perfect_collinearity
    if type(remove_perfect_collinearity) is not bool:
        sys.exit('(Type Error): remove_perfect_collinearity parameter only accepts True or False.')
        
    #html
    if type(html) is not bool:
        sys.exit('(Type Error): html parameter only accepts True or False.')

    #folds_shuffle
    if type(folds_shuffle) is not bool:
        sys.exit('(Type Error): folds_shuffle parameter only accepts True or False.')

    #data_split_shuffle
    if type(data_split_shuffle) is not bool:
        sys.exit('(Type Error): data_split_shuffle parameter only accepts True or False.')

    #log_experiment
    if type(log_experiment) is not bool:
        sys.exit('(Type Error): log_experiment parameter only accepts True or False.')

    #log_plots
    if type(log_plots) is not bool:
        sys.exit('(Type Error): log_plots parameter only accepts True or False.')

    #log_data
    if type(log_data) is not bool:
        sys.exit('(Type Error): log_data parameter only accepts True or False.')

    #log_profile
    if type(log_profile) is not bool:
        sys.exit('(Type Error): log_profile parameter only accepts True or False.')

    logger.info("Preloading libraries")

    #pre-load libraries
    import pandas as pd
    import ipywidgets as ipw
    from IPython.display import display, HTML, clear_output, update_display
    import datetime, time
    import os

    #pandas option
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.max_rows', 500)
    
    #global html_param
    global html_param
    
    #create html_param
    html_param = html

    #silent parameter to also set sampling to False
    if silent:
        sampling = False

    logger.info("Preparing display monitor")

    #progress bar
    if sampling:
        max = 10 + 3
    else:
        max = 3
        
    progress = ipw.IntProgress(value=0, min=0, max=max, step=1 , description='Processing: ')
    if verbose:
        if html_param:
            display(progress)
    
    timestampStr = datetime.datetime.now().strftime("%H:%M:%S")
    monitor = pd.DataFrame( [ ['Initiated' , '. . . . . . . . . . . . . . . . . .', timestampStr ], 
                             ['Status' , '. . . . . . . . . . . . . . . . . .' , 'Loading Dependencies' ],
                             ['ETC' , '. . . . . . . . . . . . . . . . . .',  'Calculating ETC'] ],
                              columns=['', ' ', '   ']).set_index('')
    
    if verbose:
        if html_param:
            display(monitor, display_id = 'monitor')
    
    logger.info("Importing libraries")

    #general dependencies
    import numpy as np
    from sklearn.linear_model import LinearRegression
    from sklearn.model_selection import train_test_split
    from sklearn import metrics
    import random
    import seaborn as sns
    import matplotlib.pyplot as plt
    import plotly.express as px
    
    #setting sklearn config to print all parameters including default
    import sklearn
    sklearn.set_config(print_changed_only=False)
    
    #define highlight function for function grid to display
    def highlight_max(s):
        is_max = s == True
        return ['background-color: yellow' if v else '' for v in is_max]
    
    #cufflinks
    import cufflinks as cf
    cf.go_offline()
    cf.set_config_file(offline=False, world_readable=True)
    
    #ignore warnings
    import warnings
    warnings.filterwarnings('ignore') 
    

    logger.info("Declaring global variables")

    #declaring global variables to be accessed by other functions
    global X, y, X_train, X_test, y_train, y_test, seed, prep_pipe, target_inverse_transformer, experiment__,\
        preprocess, folds_shuffle_param, n_jobs_param, create_model_container, master_model_container,\
        display_container, exp_name_log, logging_param, log_plots_param, data_before_preprocess, target_param,\
        gpu_param

    logger.info("Copying data for preprocessing")
    #copy original data for pandas profiler
    data_before_preprocess = data.copy()
    
    #generate seed to be used globally
    if session_id is None:
        seed = random.randint(150,9000)
    else:
        seed = session_id
    

    """
    preprocessing starts here
    """
    
    monitor.iloc[1,1:] = 'Preparing Data for Modeling'
    if verbose:
        if html_param:
            update_display(monitor, display_id = 'monitor')
            
    #define parameters for preprocessor
    
    logger.info("Declaring preprocessing parameters")

    #categorical features
    if categorical_features is None:
        cat_features_pass = []
    else:
        cat_features_pass = categorical_features
    
    #numeric features
    if numeric_features is None:
        numeric_features_pass = []
    else:
        numeric_features_pass = numeric_features
     
    #drop features
    if ignore_features is None:
        ignore_features_pass = []
    else:
        ignore_features_pass = ignore_features
     
    #date features
    if date_features is None:
        date_features_pass = []
    else:
        date_features_pass = date_features
        
    #categorical imputation strategy
    if categorical_imputation == 'constant':
        categorical_imputation_pass = 'not_available'
    elif categorical_imputation == 'mode':
        categorical_imputation_pass = 'most frequent'
    
    #transformation method strategy
    if transformation_method == 'yeo-johnson':
        trans_method_pass = 'yj'
    elif transformation_method == 'quantile':
        trans_method_pass = 'quantile'
    
    #pass method
    if pca_method == 'linear':
        pca_method_pass = 'pca_liner'
            
    elif pca_method == 'kernel':
        pca_method_pass = 'pca_kernal'
            
    elif pca_method == 'incremental':
        pca_method_pass = 'incremental'
            
    elif pca_method == 'pls':
        pca_method_pass = 'pls'
        
    #pca components
    if pca is True:
        if pca_components is None:
            if pca_method == 'linear':
                pca_components_pass = 0.99
            else:
                pca_components_pass = int((len(data.columns)-1)*0.5)
                
        else:
            pca_components_pass = pca_components
            
    else:
        pca_components_pass = 0.99
        
    if bin_numeric_features is None:
        apply_binning_pass = False
        features_to_bin_pass = []
    
    else:
        apply_binning_pass = True
        features_to_bin_pass = bin_numeric_features
    
    #trignometry
    if trigonometry_features is False:
        trigonometry_features_pass = []
    else:
        trigonometry_features_pass = ['sin', 'cos', 'tan']
    
    #group features
    #=============#
    
    #apply grouping
    if group_features is not None:
        apply_grouping_pass = True
    else:
        apply_grouping_pass = False
    
    #group features listing
    if apply_grouping_pass is True:
        
        if type(group_features[0]) is str:
            group_features_pass = []
            group_features_pass.append(group_features)
        else:
            group_features_pass = group_features
            
    else:
        
        group_features_pass = [[]]
    
    #group names
    if apply_grouping_pass is True:

        if (group_names is None) or (len(group_names) != len(group_features_pass)):
            group_names_pass = list(np.arange(len(group_features_pass)))
            group_names_pass = ['group_' + str(i) for i in group_names_pass]

        else:
            group_names_pass = group_names
            
    else:
        group_names_pass = []
    
    #feature interactions
    
    if feature_interaction or feature_ratio:
        apply_feature_interactions_pass = True
    else:
        apply_feature_interactions_pass = False
    
    interactions_to_apply_pass = []
    
    if feature_interaction:
        interactions_to_apply_pass.append('multiply')
    
    if feature_ratio:
        interactions_to_apply_pass.append('divide')
    
    #unknown categorical
    if unknown_categorical_method == 'least_frequent':
        unknown_categorical_method_pass = 'least frequent'
    elif unknown_categorical_method == 'most_frequent':
        unknown_categorical_method_pass = 'most frequent'

    #ordinal_features
    if ordinal_features is not None:
        apply_ordinal_encoding_pass = True
    else:
        apply_ordinal_encoding_pass = False
        
    if apply_ordinal_encoding_pass is True:
        ordinal_columns_and_categories_pass = ordinal_features
    else:
        ordinal_columns_and_categories_pass = {}
    
    if high_cardinality_features is not None:
        apply_cardinality_reduction_pass = True
    else:
        apply_cardinality_reduction_pass = False
        
    if high_cardinality_method == 'frequency':
        cardinal_method_pass = 'count'
    elif high_cardinality_method == 'clustering':
        cardinal_method_pass = 'cluster'
        
    if apply_cardinality_reduction_pass:
        cardinal_features_pass = high_cardinality_features
    else:
        cardinal_features_pass = []
        
    if silent:
        display_dtypes_pass = False
    else:
        display_dtypes_pass = True
        
    #transform target method
    if transform_target_method == 'box-cox':
        transform_target_method_pass = 'bc'
    elif transform_target_method == 'yeo-johnson':
        transform_target_method_pass = 'yj'

    logger.info("Importing preprocessing module")
    
    #import library
    import pycaret.preprocess as preprocess
    
    logger.info("Creating preprocessing pipeline")

    data = preprocess.Preprocess_Path_One(train_data = data, 
                                          target_variable = target,
                                          categorical_features = cat_features_pass,
                                          apply_ordinal_encoding = apply_ordinal_encoding_pass, 
                                          ordinal_columns_and_categories = ordinal_columns_and_categories_pass, 
                                          apply_cardinality_reduction = apply_cardinality_reduction_pass,
                                          cardinal_method = cardinal_method_pass, 
                                          cardinal_features = cardinal_features_pass,
                                          numerical_features = numeric_features_pass,
                                          time_features = date_features_pass,
                                          features_todrop = ignore_features_pass,
                                          numeric_imputation_strategy = numeric_imputation,
                                          categorical_imputation_strategy = categorical_imputation_pass,
                                          scale_data = normalize,
                                          scaling_method = normalize_method,
                                          Power_transform_data = transformation,
                                          Power_transform_method = trans_method_pass,
                                          apply_untrained_levels_treatment= handle_unknown_categorical,
                                          untrained_levels_treatment_method = unknown_categorical_method_pass, 
                                          apply_pca = pca, 
                                          pca_method = pca_method_pass, 
                                          pca_variance_retained_or_number_of_components = pca_components_pass, 
                                          apply_zero_nearZero_variance = ignore_low_variance,
                                          club_rare_levels = combine_rare_levels,
                                          rara_level_threshold_percentage = rare_level_threshold,
                                          apply_binning = apply_binning_pass,
                                          features_to_binn = features_to_bin_pass,
                                          remove_outliers = remove_outliers,
                                          outlier_contamination_percentage = outliers_threshold,
                                          outlier_methods = ['pca'], #pca hardcoded
                                          remove_multicollinearity = remove_multicollinearity,
                                          maximum_correlation_between_features = multicollinearity_threshold,
                                          remove_perfect_collinearity = remove_perfect_collinearity, 
                                          cluster_entire_data = create_clusters, 
                                          range_of_clusters_to_try = cluster_iter, 
                                          apply_polynomial_trigonometry_features = polynomial_features, 
                                          max_polynomial = polynomial_degree, 
                                          trigonometry_calculations = trigonometry_features_pass, 
                                          top_poly_trig_features_to_select_percentage = polynomial_threshold, 
                                          apply_grouping = apply_grouping_pass, 
                                          features_to_group_ListofList = group_features_pass, 
                                          group_name = group_names_pass, 
                                          apply_feature_selection = feature_selection, 
                                          feature_selection_top_features_percentage = feature_selection_threshold, 
                                          apply_feature_interactions = apply_feature_interactions_pass, 
                                          feature_interactions_to_apply = interactions_to_apply_pass, 
                                          feature_interactions_top_features_to_select_percentage=interaction_threshold, 
                                          display_types = display_dtypes_pass, 
                                          target_transformation = transform_target, 
                                          target_transformation_method = transform_target_method_pass, 
                                          random_state = seed)

    progress.value += 1
    logger.info("Preprocessing pipeline created successfully")
    
    if hasattr(preprocess.dtypes, 'replacement'):
            label_encoded = preprocess.dtypes.replacement
            label_encoded = str(label_encoded).replace("'", '')
            label_encoded = str(label_encoded).replace("{", '')
            label_encoded = str(label_encoded).replace("}", '')

    else:
        label_encoded = 'None'

    try:
        res_type = ['quit','Quit','exit','EXIT','q','Q','e','E','QUIT','Exit']
        res = preprocess.dtypes.response
        if res in res_type:
            sys.exit("(Process Exit): setup has been interupted with user command 'quit'. setup must rerun." )
    except:
        pass
    
    #save prep pipe
    prep_pipe = preprocess.pipe
    

    #save target inverse transformer
    try:
        target_inverse_transformer = preprocess.pt_target.p_transform_target
    except:
        target_inverse_transformer = None
        logger.info("No inverse transformer found")

    
    logger.info("Creating grid variables")

    #generate values for grid show
    missing_values = data_before_preprocess.isna().sum().sum()
    if missing_values > 0:
        missing_flag = True
    else:
        missing_flag = False
    
    if normalize is True:
        normalize_grid = normalize_method
    else:
        normalize_grid = 'None'
        
    if transformation is True:
        transformation_grid = transformation_method
    else:
        transformation_grid = 'None'
    
    if pca is True:
        pca_method_grid = pca_method
    else:
        pca_method_grid = 'None'
   
    if pca is True:
        pca_components_grid = pca_components_pass
    else:
        pca_components_grid = 'None'
    
    if combine_rare_levels:
        rare_level_threshold_grid = rare_level_threshold
    else:
        rare_level_threshold_grid = 'None'
    
    if bin_numeric_features is None:
        numeric_bin_grid = False
    else:
        numeric_bin_grid = True
    
    if remove_outliers is False:
        outliers_threshold_grid = None
    else:
        outliers_threshold_grid = outliers_threshold
    
    if remove_multicollinearity is False:
        multicollinearity_threshold_grid = None
    else:
        multicollinearity_threshold_grid = multicollinearity_threshold
    
    if create_clusters is False:
        cluster_iter_grid = None
    else:
        cluster_iter_grid = cluster_iter
    
    if polynomial_features:
        polynomial_degree_grid = polynomial_degree
    else:
        polynomial_degree_grid = None
    
    if polynomial_features or trigonometry_features:
        polynomial_threshold_grid = polynomial_threshold
    else:
        polynomial_threshold_grid = None
    
    if feature_selection:
        feature_selection_threshold_grid = feature_selection_threshold
    else:
        feature_selection_threshold_grid = None
    
    if feature_interaction or feature_ratio:
        interaction_threshold_grid = interaction_threshold
    else:
        interaction_threshold_grid = None
        
    if ordinal_features is not None:
        ordinal_features_grid = True
    else:
        ordinal_features_grid = False
        
    if handle_unknown_categorical:
        unknown_categorical_method_grid = unknown_categorical_method
    else:
        unknown_categorical_method_grid = None
       
    if group_features is not None:
        group_features_grid = True
    else:
        group_features_grid = False
        
    if high_cardinality_features is not None:
        high_cardinality_features_grid = True
    else:
        high_cardinality_features_grid = False
    
    if high_cardinality_features_grid:
        high_cardinality_method_grid = high_cardinality_method
    else:
        high_cardinality_method_grid = None
        
    learned_types = preprocess.dtypes.learent_dtypes
    learned_types.drop(target, inplace=True)

    float_type = 0 
    cat_type = 0

    for i in preprocess.dtypes.learent_dtypes:
        if 'float' in str(i):
            float_type += 1
        elif 'object' in str(i):
            cat_type += 1
        elif 'int' in str(i):
            float_type += 1
    
    #target transformation method
    if transform_target is False:
        transform_target_method_grid = None
    else:
        transform_target_method_grid = preprocess.pt_target.function_to_apply
    
    """
    preprocessing ends here
    """
    
    #reset pandas option
    pd.reset_option("display.max_rows")
    pd.reset_option("display.max_columns")
    
    logger.info("Creating global containers")

    #create an empty list for pickling later.
    experiment__ = []
    
    #create folds_shuffle_param
    folds_shuffle_param = folds_shuffle

    #create n_jobs_param
    n_jobs_param = n_jobs

    #create create_model_container
    create_model_container = []

    #create master_model_container
    master_model_container = []

    #create display container
    display_container = []

    #create logging parameter
    logging_param = log_experiment

    #create exp_name_log param incase logging is False
    exp_name_log = 'no_logging'

    #create an empty log_plots_param
    if log_plots:
        log_plots_param = True
    else:
        log_plots_param = False

    # create target param
    target_param = target

    # create gpu param
    gpu_param = use_gpu

    #sample estimator
    if sample_estimator is None:
        model = LinearRegression(n_jobs=n_jobs_param)
    else:
        model = sample_estimator
        
    model_name = str(model).split("(")[0]
    
    if 'CatBoostRegressor' in model_name:
        model_name = 'CatBoostRegressor'
        
    #creating variables to be used later in the function
    X = data.drop(target,axis=1)
    y = data[target]
    
    progress.value += 1
    
    if sampling is True and data.shape[0] > 25000: #change back to 25000
    
        split_perc = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,0.99]
        split_perc_text = ['10%','20%','30%','40%','50%','60%', '70%', '80%', '90%', '100%']
        split_perc_tt = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,0.99]
        split_perc_tt_total = []
        split_percent = []

        metric_results = []
        metric_name = []
        
        counter = 0
        
        for i in split_perc:
            
            progress.value += 1
            
            t0 = time.time()
            
            '''
            MONITOR UPDATE STARTS
            '''
            
            perc_text = split_perc_text[counter]
            monitor.iloc[1,1:] = 'Fitting Model on ' + perc_text + ' sample'
            if verbose:
                if html_param:
                    update_display(monitor, display_id = 'monitor')

            '''
            MONITOR UPDATE ENDS
            '''
    
            X_, X__, y_, y__ = train_test_split(X, y, test_size=1-i, random_state=seed, shuffle=data_split_shuffle)
            X_train, X_test, y_train, y_test = train_test_split(X_, y_, test_size=0.3, random_state=seed, shuffle=data_split_shuffle)
            model.fit(X_train,y_train)
            pred_ = model.predict(X_test)
            
            r2 = metrics.r2_score(y_test,pred_)
            metric_results.append(r2)
            metric_name.append('R2')
            split_percent.append(i)
            
            t1 = time.time()
                       
            '''
            Time calculation begins
            '''
          
            tt = t1 - t0
            total_tt = tt / i
            split_perc_tt.pop(0)
            
            for remain in split_perc_tt:
                ss = total_tt * remain
                split_perc_tt_total.append(ss)
                
            ttt = sum(split_perc_tt_total) / 60
            ttt = np.around(ttt, 2)
        
            if ttt < 1:
                ttt = str(np.around((ttt * 60), 2))
                ETC = ttt + ' Seconds Remaining'

            else:
                ttt = str (ttt)
                ETC = ttt + ' Minutes Remaining'
                
            monitor.iloc[2,1:] = ETC
            if verbose:
                if html_param:
                    update_display(monitor, display_id = 'monitor')
            
            
            '''
            Time calculation Ends
            '''
            
            split_perc_tt_total = []
            counter += 1

        model_results = pd.DataFrame({'Sample' : split_percent, 'Metric' : metric_results, 'Metric Name': metric_name})
        fig = px.line(model_results, x='Sample', y='Metric', color='Metric Name', line_shape='linear', range_y = [0,1])
        fig.update_layout(plot_bgcolor='rgb(245,245,245)')
        title= str(model_name) + ' Metric and Sample %'
        fig.update_layout(title={'text': title, 'y':0.95,'x':0.45,'xanchor': 'center','yanchor': 'top'})
        fig.show()
        
        monitor.iloc[1,1:] = 'Waiting for input'
        if verbose:
            if html_param:
                update_display(monitor, display_id = 'monitor')
        
        
        print('Please Enter the sample % of data you would like to use for modeling. Example: Enter 0.3 for 30%.')
        print('Press Enter if you would like to use 100% of the data.')
        
        print(' ')
        
        sample_size = input("Sample Size: ")
        
        if sample_size == '' or sample_size == '1':
            
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=1-train_size, random_state=seed, shuffle=data_split_shuffle)

        else:
            
            sample_n = float(sample_size)
            X_selected, X_discard, y_selected, y_discard = train_test_split(X, y, test_size=1-sample_n,  
                                                                random_state=seed, shuffle=data_split_shuffle)
            
            X_train, X_test, y_train, y_test = train_test_split(X_selected, y_selected, test_size=1-train_size, 
                                                                random_state=seed, shuffle=data_split_shuffle)

    else:
        
        monitor.iloc[1,1:] = 'Splitting Data'
        if verbose:
            if html_param:
                update_display(monitor, display_id = 'monitor')
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=1-train_size, random_state=seed, shuffle=data_split_shuffle)
        progress.value += 1

    '''
    Final display Starts
    '''
    clear_output()
    if verbose:
        print(' ')
    if profile:
        print('Setup Succesfully Completed. Loading Profile Now... Please Wait!')
    else:
        if verbose:
            print('Setup Succesfully Completed.')
    functions = pd.DataFrame ( [ ['session_id', seed ],
                                    ['Transform Target ', transform_target],
                                    ['Transform Target Method', transform_target_method_grid],
                                    ['Original Data', data_before_preprocess.shape ],
                                    ['Missing Values ', missing_flag],
                                    ['Numeric Features ', str(float_type) ],
                                    ['Categorical Features ', str(cat_type) ],
                                    ['Ordinal Features ', ordinal_features_grid],
                                    ['High Cardinality Features ', high_cardinality_features_grid],
                                    ['High Cardinality Method ', high_cardinality_method_grid],
                                    ['Sampled Data', '(' + str(X_train.shape[0] + X_test.shape[0]) + ', ' + str(data_before_preprocess.shape[1]) + ')' ], 
                                    ['Transformed Train Set', X_train.shape ], 
                                    ['Transformed Test Set',X_test.shape ],
                                    ['Numeric Imputer ', numeric_imputation],
                                    ['Categorical Imputer ', categorical_imputation],
                                    ['Normalize ', normalize ],
                                    ['Normalize Method ', normalize_grid ],
                                    ['Transformation ', transformation ],
                                    ['Transformation Method ', transformation_grid ],
                                    ['PCA ', pca],
                                    ['PCA Method ', pca_method_grid],
                                    ['PCA Components ', pca_components_grid],
                                    ['Ignore Low Variance ', ignore_low_variance],
                                    ['Combine Rare Levels ', combine_rare_levels],
                                    ['Rare Level Threshold ', rare_level_threshold_grid],
                                    ['Numeric Binning ', numeric_bin_grid],
                                    ['Remove Outliers ', remove_outliers],
                                    ['Outliers Threshold ', outliers_threshold_grid],
                                    ['Remove Multicollinearity ', remove_multicollinearity],
                                    ['Multicollinearity Threshold ', multicollinearity_threshold_grid],
                                    ['Clustering ', create_clusters],
                                    ['Clustering Iteration ', cluster_iter_grid],
                                    ['Polynomial Features ', polynomial_features],
                                    ['Polynomial Degree ', polynomial_degree_grid],
                                    ['Trignometry Features ', trigonometry_features],
                                    ['Polynomial Threshold ', polynomial_threshold_grid], 
                                    ['Group Features ', group_features_grid],
                                    ['Feature Selection ', feature_selection],
                                    ['Features Selection Threshold ', feature_selection_threshold_grid],
                                    ['Feature Interaction ', feature_interaction],
                                    ['Feature Ratio ', feature_ratio],
                                    ['Interaction Threshold ', interaction_threshold_grid],
                                ], columns = ['Description', 'Value'] )
    
    functions_ = functions.style.apply(highlight_max)
    if verbose:
        if html_param:
            display(functions_)
        else:
            print(functions_.data)
        
    if profile:
        try:
            import pandas_profiling
            pf = pandas_profiling.ProfileReport(data_before_preprocess)
            clear_output()
            display(pf)
        except:
            print('Data Profiler Failed. No output to show, please continue with Modeling.')
        
    '''
    Final display Ends
    '''   
    
    #log into experiment
    experiment__.append(('Regression Setup Config', functions))
    experiment__.append(('X_training Set', X_train))
    experiment__.append(('y_training Set', y_train))
    experiment__.append(('X_test Set', X_test))
    experiment__.append(('y_test Set', y_test))
    experiment__.append(('Transformation Pipeline', prep_pipe))
    try:
        experiment__.append(('Target Inverse Transformer', target_inverse_transformer))
    except:
        pass
        
    #end runtime
    runtime_end = time.time()
    runtime = np.array(runtime_end - runtime_start).round(2)

    if logging_param:
        
        logger.info("Logging experiment in MLFlow")
        
        import mlflow
        from pathlib import Path

        if experiment_name is None:
            exp_name_ = 'reg-default-name'
        else:
            exp_name_ = experiment_name

        URI = secrets.token_hex(nbytes=4)    
        exp_name_log = exp_name_
        
        try:
            mlflow.create_experiment(exp_name_log)
        except:
            pass

        #mlflow logging
        mlflow.set_experiment(exp_name_log)

        run_name_ = 'Session Initialized ' + str(USI)
        with mlflow.start_run(run_name=run_name_) as run:

            # Get active run to log as tag
            RunID = mlflow.active_run().info.run_id
            
            k = functions.copy()
            k.set_index('Description',drop=True,inplace=True)
            kdict = k.to_dict()
            params = kdict.get('Value')
            mlflow.log_params(params)

            #set tag of compare_models
            mlflow.set_tag("Source", "setup")
            
            import secrets
            URI = secrets.token_hex(nbytes=4)
            mlflow.set_tag("URI", URI)
            mlflow.set_tag("USI", USI) 
            mlflow.set_tag("Run Time", runtime)
            mlflow.set_tag("Run ID", RunID)

            # Log the transformation pipeline
            logger.info("SubProcess save_model() called ==================================")
            save_model(prep_pipe, 'Transformation Pipeline', verbose=False)
            logger.info("SubProcess save_model() end ==================================")
            mlflow.log_artifact('Transformation Pipeline' + '.pkl')
            os.remove('Transformation Pipeline.pkl')

            # Log pandas profile
            if log_profile:
                import pandas_profiling
                pf = pandas_profiling.ProfileReport(data_before_preprocess)
                pf.to_file("Data Profile.html")
                mlflow.log_artifact("Data Profile.html")
                os.remove("Data Profile.html")
                clear_output()
                display(functions_)

            # Log training and testing set
            if log_data:
                X_train.join(y_train).to_csv('Train.csv')
                X_test.join(y_test).to_csv('Test.csv')
                mlflow.log_artifact("Train.csv")
                mlflow.log_artifact("Test.csv")
                os.remove('Train.csv')
                os.remove('Test.csv')

    logger.info("create_model_container: " + str(len(create_model_container)))
    logger.info("master_model_container: " + str(len(master_model_container)))
    logger.info("display_container: " + str(len(display_container)))

    logger.info("setup() succesfully completed......................................")

    return X, y, X_train, X_test, y_train, y_test, seed, prep_pipe, target_inverse_transformer,\
        experiment__, folds_shuffle_param, n_jobs_param, html_param, create_model_container,\
        master_model_container, display_container, exp_name_log, logging_param, log_plots_param, USI,\
        data_before_preprocess, target_param

def compare_models(blacklist = None,
                   whitelist = None, #added in pycaret==2.0.0
                   fold = 10, 
                   round = 4, 
                   sort = 'R2',
                   n_select = 1, #added in pycaret==2.0.0
                   turbo = True,
                   verbose = True): #added in pycaret==2.0.0
    
    """
    This function train all the models available in the model library and scores them 
    using Kfold Cross Validation. The output prints a score grid with MAE, MSE 
    RMSE, R2, RMSLE and MAPE (averaged accross folds), determined by fold parameter.
    
    This function returns the best model based on metric defined in sort parameter. 
    
    To select top N models, use n_select parameter that is set to 1 by default.
    Where n_select parameter > 1, it will return a list of trained model objects.

    When turbo is set to True ('kr', 'ard' and 'mlp') are excluded due to longer
    training times. By default turbo param is set to True.

    Example
    --------
    >>> from pycaret.datasets import get_data
    >>> boston = get_data('boston')
    >>> experiment_name = setup(data = boston,  target = 'medv')
    >>> best_model = compare_models() 

    This will return the averaged score grid of all models except 'kr', 'ard' 
    and 'mlp'. When turbo param is set to False, all models including 'kr',
    'ard' and 'mlp' are used, but this may result in longer training times.
    
    >>> best_model = compare_models(blacklist = ['knn','gbr'], turbo = False) 

    This will return a comparison of all models except K Nearest Neighbour and
    Gradient Boosting Regressor.
    
    >>> best_model = compare_models(blacklist = ['knn','gbr'] , turbo = True) 

    This will return a comparison of all models except K Nearest Neighbour, 
    Gradient Boosting Regressor, Kernel Ridge Regressor, Automatic Relevance
    Determinant and Multi Level Perceptron.
        
    Parameters
    ----------
    blacklist: list of strings, default = None
        In order to omit certain models from the comparison model ID's can be passed as 
        a list of strings in blacklist param. 

    whitelist: list of strings, default = None
        In order to run only certain models for the comparison, the model ID's can be 
        passed as a list of strings in whitelist param. 

    fold: integer, default = 10
        Number of folds to be used in Kfold CV. Must be at least 2. 

    round: integer, default = 4
        Number of decimal places the metrics in the score grid will be rounded to.
  
    sort: string, default = 'MAE'
        The scoring measure specified is used for sorting the average score grid
        Other options are 'MAE', 'MSE', 'RMSE', 'R2', 'RMSLE' and 'MAPE'.

    n_select: int, default = 1
        Number of top_n models to return. use negative argument for bottom selection.
        for example, n_select = -3 means bottom 3 models.

    turbo: Boolean, default = True
        When turbo is set to True, it blacklists estimators that have longer
        training times.

    verbose: Boolean, default = True
        Score grid is not printed when verbose is set to False.
    
    Returns
    -------
    score_grid
        A table containing the scores of the model across the kfolds. 
        Scoring metrics used are MAE, MSE, RMSE, R2, RMSLE and MAPE
        Mean and standard deviation of the scores across the folds is
        also returned.

    Warnings
    --------
    - compare_models() though attractive, might be time consuming with large 
      datasets. By default turbo is set to True, which blacklists models that
      have longer training times. Changing turbo parameter to False may result 
      in very high training times with datasets where number of samples exceed 
      10,000.
             
    
    """
    
    '''
    
    ERROR HANDLING STARTS HERE
    
    '''
    
    import logging

    try:
        hasattr(logger, 'name')
    except:
        logger = logging.getLogger('logs')
        logger.setLevel(logging.DEBUG)
        
        # create console handler and set level to debug
        if logger.hasHandlers():
            logger.handlers.clear()
        
        ch = logging.FileHandler('logs.log')
        ch.setLevel(logging.DEBUG)

        # create formatter
        formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        logger.addHandler(ch)

    logger.info("Initializing compare_models()")
    logger.info("""compare_models(blacklist={}, whitelist={}, fold={}, round={}, sort={}, n_select={}, turbo={}, verbose={})""".\
        format(str(blacklist), str(whitelist), str(fold), str(round), str(sort), str(n_select), str(turbo), str(verbose)))

    logger.info("Checking exceptions")

    #exception checking   
    import sys
    
    #checking error for blacklist (string)
    available_estimators = ['lr', 'lasso', 'ridge', 'en', 'lar', 'llar', 'omp', 'br', 'ard', 'par', 
                            'ransac', 'tr', 'huber', 'kr', 'svm', 'knn', 'dt', 'rf', 'et', 'ada', 'gbr', 
                            'mlp', 'xgboost', 'lightgbm', 'catboost']

    if blacklist != None:
        for i in blacklist:
            if i not in available_estimators:
                sys.exit('(Value Error): Estimator Not Available. Please see docstring for list of available estimators.')

    if whitelist != None:   
        for i in whitelist:
            if i not in available_estimators:
                sys.exit('(Value Error): Estimator Not Available. Please see docstring for list of available estimators.')

    #whitelist and blacklist together check
    if whitelist is not None:
        if blacklist is not None:
            sys.exit('(Type Error): Cannot use blacklist parameter when whitelist is used to compare models.')

    #checking fold parameter
    if type(fold) is not int:
        sys.exit('(Type Error): Fold parameter only accepts integer value.')
    
    #checking round parameter
    if type(round) is not int:
        sys.exit('(Type Error): Round parameter only accepts integer value.')
 
    #checking sort parameter
    allowed_sort = ['MAE', 'MSE', 'RMSE', 'R2', 'RMSLE', 'MAPE']
    if sort not in allowed_sort:
        sys.exit('(Value Error): Sort method not supported. See docstring for list of available parameters.')
    
    
    '''

    ERROR HANDLING ENDS HERE
    
    '''
    
    logger.info("Preloading libraries")

    #pre-load libraries
    import pandas as pd
    import time, datetime
    import ipywidgets as ipw
    from IPython.display import display, HTML, clear_output, update_display
    
    pd.set_option('display.max_columns', 500)

    logger.info("Preparing display monitor")

    #progress bar
    if blacklist is None:
        len_of_blacklist = 0
    else:
        len_of_blacklist = len(blacklist)
        
    if turbo:
        len_mod = 22 - len_of_blacklist
    else:
        len_mod = 25 - len_of_blacklist

    #n_select param
    if type(n_select) is list:
        n_select_num = len(n_select)
    else:
        n_select_num = abs(n_select)

    if n_select_num > len_mod:
        n_select_num = len_mod

    if whitelist is not None:
        wl = len(whitelist)
        bl = len_of_blacklist
        len_mod = wl - bl

    if whitelist is not None:
        opt = 10
    else:
        opt = 30
        
    #display
    progress = ipw.IntProgress(value=0, min=0, max=(fold*len_mod)+opt+n_select_num, step=1 , description='Processing: ')
    master_display = pd.DataFrame(columns=['Model', 'MAE','MSE','RMSE', 'R2', 'RMSLE', 'MAPE', 'TT (Sec)'])
    
    #display monitor only when html_param is set to True
    if verbose:
        if html_param:
            display(progress)
    
    timestampStr = datetime.datetime.now().strftime("%H:%M:%S")
    monitor = pd.DataFrame( [ ['Initiated' , '. . . . . . . . . . . . . . . . . .', timestampStr ], 
                             ['Status' , '. . . . . . . . . . . . . . . . . .' , 'Loading Dependencies' ],
                             ['Estimator' , '. . . . . . . . . . . . . . . . . .' , 'Compiling Library' ],
                             ['ETC' , '. . . . . . . . . . . . . . . . . .',  'Calculating ETC'] ],
                              columns=['', ' ', '   ']).set_index('')
    
    #display only when html_param is set to True
    if verbose:
        if html_param:
            display(monitor, display_id = 'monitor')
            display_ = display(master_display, display_id=True)
            display_id = display_.display_id
    
    
    #ignore warnings
    import warnings
    warnings.filterwarnings('ignore') 
    
    #general dependencies
    import numpy as np
    import random
    from sklearn import metrics
    from sklearn.model_selection import KFold
    import pandas.io.formats.style
    
    logger.info("Copying training dataset")
    #Storing X_train and y_train in data_X and data_y parameter
    data_X = X_train.copy()
    data_y = y_train.copy()
    
    #reset index
    data_X.reset_index(drop=True, inplace=True)
    data_y.reset_index(drop=True, inplace=True)
    
    progress.value += 1
    
    logger.info("Importing libraries")
    #import sklearn dependencies
    from sklearn.linear_model import LinearRegression
    from sklearn.linear_model import Ridge
    from sklearn.linear_model import Lasso
    from sklearn.linear_model import ElasticNet
    from sklearn.linear_model import Lars
    from sklearn.linear_model import LassoLars
    from sklearn.linear_model import OrthogonalMatchingPursuit
    from sklearn.linear_model import BayesianRidge
    from sklearn.linear_model import ARDRegression
    from sklearn.linear_model import PassiveAggressiveRegressor
    from sklearn.linear_model import RANSACRegressor
    from sklearn.linear_model import TheilSenRegressor
    from sklearn.linear_model import HuberRegressor
    from sklearn.kernel_ridge import KernelRidge
    from sklearn.svm import SVR
    from sklearn.neighbors import KNeighborsRegressor
    from sklearn.tree import DecisionTreeRegressor
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.ensemble import ExtraTreesRegressor
    from sklearn.ensemble import AdaBoostRegressor
    from sklearn.ensemble import GradientBoostingRegressor
    from sklearn.neural_network import MLPRegressor
    from xgboost import XGBRegressor
    from catboost import CatBoostRegressor
    try:
        import lightgbm as lgb
    except:
        pass
        logger.info("LightGBM import failed")
   
    progress.value += 1

    
    '''
    MONITOR UPDATE STARTS
    '''
    
    monitor.iloc[1,1:] = 'Loading Estimator'
    if verbose:
        if html_param:
            update_display(monitor, display_id = 'monitor')
    
    '''
    MONITOR UPDATE ENDS
    '''
    
    logger.info("Importing untrained models")

    #creating model object
    lr = LinearRegression(n_jobs=n_jobs_param)
    lasso = Lasso(random_state=seed)
    ridge = Ridge(random_state=seed)
    en = ElasticNet(random_state=seed)
    lar = Lars()
    llar = LassoLars()
    omp = OrthogonalMatchingPursuit()
    br = BayesianRidge()
    ard = ARDRegression()
    par = PassiveAggressiveRegressor(random_state=seed)
    ransac = RANSACRegressor(min_samples=0.5, random_state=seed)
    tr = TheilSenRegressor(random_state=seed, n_jobs=n_jobs_param)
    huber = HuberRegressor()
    kr = KernelRidge()
    svm = SVR()
    knn = KNeighborsRegressor(n_jobs=n_jobs_param)
    dt = DecisionTreeRegressor(random_state=seed)
    rf = RandomForestRegressor(random_state=seed, n_jobs=n_jobs_param)
    et = ExtraTreesRegressor(random_state=seed, n_jobs=n_jobs_param)
    ada = AdaBoostRegressor(random_state=seed)
    gbr = GradientBoostingRegressor(random_state=seed)
    mlp = MLPRegressor(random_state=seed)
    xgboost = XGBRegressor(random_state=seed, n_jobs=n_jobs_param, verbosity=0)
    lightgbm = lgb.LGBMRegressor(random_state=seed, n_jobs=n_jobs_param)
    catboost = CatBoostRegressor(random_state=seed, silent = True, thread_count=n_jobs_param)
    
    logger.info("Import successful")

    progress.value += 1
    
    model_dict = {'Linear Regression' : 'lr',
                   'Lasso Regression' : 'lasso', 
                   'Ridge Regression' : 'ridge', 
                   'Elastic Net' : 'en',
                   'Least Angle Regression' : 'lar', 
                   'Lasso Least Angle Regression' : 'llar', 
                   'Orthogonal Matching Pursuit' : 'omp', 
                   'Bayesian Ridge' : 'br', 
                   'Automatic Relevance Determination' : 'ard',
                   'Passive Aggressive Regressor' : 'par', 
                   'Random Sample Consensus' : 'ransac',
                   'TheilSen Regressor' : 'tr', 
                   'Huber Regressor' : 'huber', 
                   'Kernel Ridge' : 'kr',
                   'Support Vector Machine' : 'svm', 
                   'K Neighbors Regressor' : 'knn', 
                   'Decision Tree' : 'dt', 
                   'Random Forest' : 'rf', 
                   'Extra Trees Regressor' : 'et',
                   'AdaBoost Regressor' : 'ada',
                   'Gradient Boosting Regressor' : 'gbr', 
                   'Multi Level Perceptron' : 'mlp',
                   'Extreme Gradient Boosting' : 'xgboost',
                   'Light Gradient Boosting Machine' :  'lightgbm',
                   'CatBoost Regressor' : 'catboost'}
    
    model_library = [lr, lasso, ridge, en, lar, llar, omp, br, ard, par, ransac, tr, huber, kr, 
                     svm, knn, dt, rf, et, ada, gbr, mlp, xgboost, lightgbm, catboost]
    
    model_names = ['Linear Regression',
                   'Lasso Regression',
                   'Ridge Regression',
                   'Elastic Net',
                   'Least Angle Regression',
                   'Lasso Least Angle Regression',
                   'Orthogonal Matching Pursuit',
                   'Bayesian Ridge',
                   'Automatic Relevance Determination',
                   'Passive Aggressive Regressor',
                   'Random Sample Consensus',
                   'TheilSen Regressor',
                   'Huber Regressor',
                   'Kernel Ridge',
                   'Support Vector Machine',
                   'K Neighbors Regressor',
                   'Decision Tree',
                   'Random Forest',
                   'Extra Trees Regressor',
                   'AdaBoost Regressor',
                   'Gradient Boosting Regressor',
                   'Multi Level Perceptron',
                   'Extreme Gradient Boosting',
                   'Light Gradient Boosting Machine',
                   'CatBoost Regressor']
    
    
    #checking for blacklist models
    
    model_library_str = ['lr', 'lasso', 'ridge', 'en', 'lar', 'llar', 'omp', 'br', 'ard',
                         'par', 'ransac', 'tr', 'huber', 'kr', 'svm', 'knn', 'dt', 'rf', 
                         'et', 'ada', 'gbr', 'mlp', 'xgboost', 'lightgbm', 'catboost']
    
    model_library_str_ = ['lr', 'lasso', 'ridge', 'en', 'lar', 'llar', 'omp', 'br', 'ard',
                         'par', 'ransac', 'tr', 'huber', 'kr', 'svm', 'knn', 'dt', 'rf', 
                         'et', 'ada', 'gbr', 'mlp', 'xgboost', 'lightgbm', 'catboost']
    
    if blacklist is not None:
        
        if turbo:
            internal_blacklist = ['kr', 'ard', 'mlp']
            compiled_blacklist = blacklist + internal_blacklist
            blacklist = list(set(compiled_blacklist))
            
        else:
            blacklist = blacklist
        
        for i in blacklist:
            model_library_str_.remove(i)
        
        si = []
        
        for i in model_library_str_:
            s = model_library_str.index(i)
            si.append(s)
        
        model_library_ = []
        model_names_= []
        for i in si:
            model_library_.append(model_library[i])
            model_names_.append(model_names[i])
            
        model_library = model_library_
        model_names = model_names_
        
        
    if blacklist is None and turbo is True:
        
        model_library = [lr, lasso, ridge, en, lar, llar, omp, br, par, ransac, tr, huber, 
                         svm, knn, dt, rf, et, ada, gbr, xgboost, lightgbm, catboost]
    
        model_names = ['Linear Regression',
                       'Lasso Regression',
                       'Ridge Regression',
                       'Elastic Net',
                       'Least Angle Regression',
                       'Lasso Least Angle Regression',
                       'Orthogonal Matching Pursuit',
                       'Bayesian Ridge',
                       'Passive Aggressive Regressor',
                       'Random Sample Consensus',
                       'TheilSen Regressor',
                       'Huber Regressor',
                       'Support Vector Machine',
                       'K Neighbors Regressor',
                       'Decision Tree',
                       'Random Forest',
                       'Extra Trees Regressor',
                       'AdaBoost Regressor',
                       'Gradient Boosting Regressor',
                       'Extreme Gradient Boosting',
                       'Light Gradient Boosting Machine',
                       'CatBoost Regressor']
    
    #checking for whitelist models
    if whitelist is not None:

        model_library = []
        model_names = []

        for i in whitelist:
            if i == 'lr':
                model_library.append(lr)
                model_names.append('Linear Regression')
            elif i == 'lasso':
                model_library.append(lasso)
                model_names.append('Lasso Regression')                
            elif i == 'ridge':
                model_library.append(ridge)
                model_names.append('Ridge Regression')   
            elif i == 'en':
                model_library.append(en)
                model_names.append('Elastic Net')   
            elif i == 'lar':
                model_library.append(lar)
                model_names.append('Least Angle Regression')   
            elif i == 'llar':
                model_library.append(llar)
                model_names.append('Lasso Least Angle Regression')
            elif i == 'omp':
                model_library.append(omp)
                model_names.append('Orthogonal Matching Pursuit')   
            elif i == 'br':
                model_library.append(br)
                model_names.append('Bayesian Ridge')
            elif i == 'ard':
                model_library.append(ard)
                model_names.append('Automatic Relevance Determination')  
            elif i == 'par':
                model_library.append(par)
                model_names.append('Passive Aggressive Regressor')
            elif i == 'ransac':
                model_library.append(ransac)
                model_names.append('Random Sample Consensus')   
            elif i == 'tr':
                model_library.append(tr)
                model_names.append('TheilSen Regressor')   
            elif i == 'huber':
                model_library.append(huber)
                model_names.append('Huber Regressor')
            elif i == 'kr':
                model_library.append(kr)
                model_names.append('Kernel Ridge')     
            elif i == 'svm':
                model_library.append(svm)
                model_names.append('Support Vector Machine')   
            elif i == 'knn':
                model_library.append(knn)
                model_names.append('K Neighbors Regressor')   
            elif i == 'dt':
                model_library.append(dt)
                model_names.append('Decision Tree')   
            elif i == 'rf':
                model_library.append(rf)
                model_names.append('Random Forest') 
            elif i == 'et':
                model_library.append(et)
                model_names.append('Extra Trees Regressor') 
            elif i == 'ada':
                model_library.append(ada)
                model_names.append('AdaBoost Regressor')  
            elif i == 'gbr':
                model_library.append(gbr)
                model_names.append('Gradient Boosting Regressor')
            elif i == 'mlp':
                model_library.append(mlp)
                model_names.append('Multi Level Perceptron')     
            elif i == 'xgboost':
                model_library.append(xgboost)
                model_names.append('Extreme Gradient Boosting')   
            elif i == 'lightgbm':
                model_library.append(lightgbm)
                model_names.append('Light Gradient Boosting Machine')   
            elif i == 'catboost':
                model_library.append(catboost)
                model_names.append('CatBoost Regressor')   
            
    progress.value += 1

    
    '''
    MONITOR UPDATE STARTS
    '''
    
    monitor.iloc[1,1:] = 'Initializing CV'
    if verbose:
        if html_param:
            update_display(monitor, display_id = 'monitor')
    
    '''
    MONITOR UPDATE ENDS
    '''
    
    #cross validation setup starts here
    logger.info("Defining folds")
    kf = KFold(fold, random_state=seed, shuffle=folds_shuffle_param)

    logger.info("Declaring metric variables")
    score_mae =np.empty((0,0))
    score_mse =np.empty((0,0))
    score_rmse =np.empty((0,0))
    score_rmsle =np.empty((0,0))
    score_r2 =np.empty((0,0))
    score_mape =np.empty((0,0))
    score_training_time=np.empty((0,0))
    avgs_mae =np.empty((0,0))
    avgs_mse =np.empty((0,0))
    avgs_rmse =np.empty((0,0))
    avgs_rmsle =np.empty((0,0))
    avgs_r2 =np.empty((0,0))
    avgs_mape =np.empty((0,0))  
    avgs_training_time=np.empty((0,0))
    
    def calculate_mape(actual, prediction):
        mask = actual != 0
        return (np.fabs(actual - prediction)/actual)[mask].mean()
    
    #create URI (before loop)
    import secrets
    URI = secrets.token_hex(nbytes=4)

    name_counter = 0

    model_store = []

    for model in model_library:

        logger.info("Initializing " + str(model_names[name_counter]))

        #run_time
        runtime_start = time.time()

        progress.value += 1
        
        '''
        MONITOR UPDATE STARTS
        '''
        monitor.iloc[2,1:] = model_names[name_counter]
        monitor.iloc[3,1:] = 'Calculating ETC'
        if verbose:
            if html_param:
                update_display(monitor, display_id = 'monitor')

        '''
        MONITOR UPDATE ENDS
        '''
        
        fold_num = 1

        model_store_by_fold = []
        
        for train_i , test_i in kf.split(data_X,data_y):

            logger.info("Initializing Fold " + str(fold_num))
        
            progress.value += 1
            
            t0 = time.time()
            
            '''
            MONITOR UPDATE STARTS
            '''
                
            monitor.iloc[1,1:] = 'Fitting Fold ' + str(fold_num) + ' of ' + str(fold)
            if verbose:
                if html_param:
                    update_display(monitor, display_id = 'monitor')
            
            '''
            MONITOR UPDATE ENDS
            '''            
     
            Xtrain,Xtest = data_X.iloc[train_i], data_X.iloc[test_i]
            ytrain,ytest = data_y.iloc[train_i], data_y.iloc[test_i]
            time_start=time.time()
            logger.info("Fitting Model")
            model_store_by_fold.append(model.fit(Xtrain,ytrain))
            logger.info("Evaluating Metrics")
            time_end=time.time()
            pred_ = model.predict(Xtest)
            
            try:
                pred_ = target_inverse_transformer.inverse_transform(np.array(pred_).reshape(-1,1))
                ytest = target_inverse_transformer.inverse_transform(np.array(ytest).reshape(-1,1))
                pred_ = np.nan_to_num(pred_)
                ytest = np.nan_to_num(ytest)

            except:
                pass
                logger.info("No inverse transformer found")

            logger.info("Compiling Metrics")
            mae = metrics.mean_absolute_error(ytest,pred_)
            mse = metrics.mean_squared_error(ytest,pred_)
            rmse = np.sqrt(mse)
            r2 = metrics.r2_score(ytest,pred_)
            rmsle = np.sqrt(np.mean(np.power(np.log(np.array(abs(pred_))+1) - np.log(np.array(abs(ytest))+1), 2)))
            mape = calculate_mape(ytest,pred_)
            training_time=time_end-time_start
            score_mae = np.append(score_mae,mae)
            score_mse = np.append(score_mse,mse)
            score_rmse = np.append(score_rmse,rmse)
            score_rmsle = np.append(score_rmsle,rmsle)
            score_r2 =np.append(score_r2,r2)
            score_mape = np.append(score_mape,mape)            
            score_training_time=np.append(score_training_time,training_time)
                
                
            '''
            TIME CALCULATION SUB-SECTION STARTS HERE
            '''
            t1 = time.time()
        
            tt = (t1 - t0) * (fold-fold_num) / 60
            tt = np.around(tt, 2)
        
            if tt < 1:
                tt = str(np.around((tt * 60), 2))
                ETC = tt + ' Seconds Remaining'
                
            else:
                tt = str (tt)
                ETC = tt + ' Minutes Remaining'
            
            fold_num += 1
            
            '''
            MONITOR UPDATE STARTS
            '''

            monitor.iloc[3,1:] = ETC
            if verbose:
                if html_param:
                    update_display(monitor, display_id = 'monitor')

            '''
            MONITOR UPDATE ENDS
            '''

        model_store.append(model_store_by_fold[0])
        
        logger.info("Calculating mean and std")
        avgs_mae = np.append(avgs_mae,np.mean(score_mae))
        avgs_mse = np.append(avgs_mse,np.mean(score_mse))
        avgs_rmse = np.append(avgs_rmse,np.mean(score_rmse))
        avgs_rmsle = np.append(avgs_rmsle,np.mean(score_rmsle))
        avgs_r2 = np.append(avgs_r2,np.mean(score_r2))
        avgs_mape = np.append(avgs_mape,np.mean(score_mape))
        avgs_training_time = np.append(avgs_training_time,np.mean(score_training_time))
        
        logger.info("Creating metrics dataframe")
        compare_models_ = pd.DataFrame({'Model':model_names[name_counter], 'MAE':avgs_mae, 'MSE':avgs_mse, 
                           'RMSE':avgs_rmse, 'R2':avgs_r2, 'RMSLE':avgs_rmsle, 'MAPE':avgs_mape, 'TT (Sec)':avgs_training_time})
        master_display = pd.concat([master_display, compare_models_],ignore_index=True)
        master_display = master_display.round(round)
        
        if sort == 'R2':
            master_display = master_display.sort_values(by=sort,ascending=False)
        else:
            master_display = master_display.sort_values(by=sort,ascending=True)

        master_display.reset_index(drop=True, inplace=True)
        
        if verbose:
            if html_param:
                update_display(master_display, display_id = display_id)
        

        #end runtime
        runtime_end = time.time()
        runtime = np.array(runtime_end - runtime_start).round(2)

        """
        MLflow logging starts here
        """

        if logging_param:

            logger.info("Creating MLFlow logs")

            import mlflow
            from pathlib import Path
            import os

            run_name = model_names[name_counter]

            with mlflow.start_run(run_name=run_name) as run:  

                # Get active run to log as tag
                RunID = mlflow.active_run().info.run_id

                params = model.get_params()

                for i in list(params):
                    v = params.get(i)
                    if len(str(v)) > 250:
                        params.pop(i)
                        
                mlflow.log_params(params)

                #set tag of compare_models
                mlflow.set_tag("Source", "compare_models")
                mlflow.set_tag("URI", URI)
                mlflow.set_tag("USI", USI)
                mlflow.set_tag("Run Time", runtime)
                mlflow.set_tag("Run ID", RunID)

                #Log top model metrics
                mlflow.log_metric("MAE", avgs_mae[0])
                mlflow.log_metric("MSE", avgs_mse[0])
                mlflow.log_metric("RMSE", avgs_rmse[0])
                mlflow.log_metric("R2", avgs_r2[0])
                mlflow.log_metric("RMSLE", avgs_rmsle[0])
                mlflow.log_metric("MAPE", avgs_mape[0])
                mlflow.log_metric("TT", avgs_training_time[0])

                # Log model and transformation pipeline
                from copy import deepcopy

                # get default conda env
                from mlflow.sklearn import get_default_conda_env
                default_conda_env = get_default_conda_env()
                default_conda_env['name'] = str(exp_name_log) + '-env'
                default_conda_env.get('dependencies').pop(-3)
                dependencies = default_conda_env.get('dependencies')[-1]
                from pycaret.utils import __version__
                dep = 'pycaret==' + str(__version__())
                dependencies['pip'] = [dep]
                
                # define model signature
                from mlflow.models.signature import infer_signature
                signature = infer_signature(data_before_preprocess.drop([target_param], axis=1))
                input_example = data_before_preprocess.drop([target_param], axis=1).iloc[0].to_dict()

                # log model as sklearn flavor
                prep_pipe_temp = deepcopy(prep_pipe)
                prep_pipe_temp.steps.append(['trained model', model])
                mlflow.sklearn.log_model(prep_pipe_temp, "model", conda_env = default_conda_env, signature = signature, input_example = input_example)
                del(prep_pipe_temp)

        score_mae =np.empty((0,0))
        score_mse =np.empty((0,0))
        score_rmse =np.empty((0,0))
        score_rmsle =np.empty((0,0))
        score_r2 =np.empty((0,0))
        score_mape =np.empty((0,0))
        score_training_time=np.empty((0,0))
        avgs_mae = np.empty((0,0))
        avgs_mse = np.empty((0,0))
        avgs_rmse = np.empty((0,0))
        avgs_rmsle = np.empty((0,0))
        avgs_r2 = np.empty((0,0))
        avgs_mape = np.empty((0,0))
        avgs_training_time=np.empty((0,0))
        name_counter += 1
  
    progress.value += 1
    
    def highlight_min(s):
        if s.name=='R2':# min
            to_highlight = s == s.max()
        else:
            to_highlight = s == s.min()

        return ['background-color: yellow' if v else '' for v in to_highlight]

    def highlight_cols(s):
        color = 'lightgrey'
        return 'background-color: %s' % color

    compare_models_ = master_display.style.apply(highlight_min,subset=['MAE','MSE','RMSE','R2','RMSLE','MAPE'])\
                                            .applymap(highlight_cols, subset = ['TT (Sec)'])
    compare_models_ = compare_models_.set_precision(round)
    compare_models_ = compare_models_.set_properties(**{'text-align': 'left'})
    compare_models_ = compare_models_.set_table_styles([dict(selector='th', props=[('text-align', 'left')])])

    progress.value += 1

    monitor.iloc[1,1:] = 'Compiling Final Model'
    monitor.iloc[3,1:] = 'Almost Finished'
    
    if verbose:
        if html_param:
            update_display(monitor, display_id = 'monitor')

    sorted_model_names = list(compare_models_.data['Model'])
    if n_select < 0:
        sorted_model_names = sorted_model_names[n_select:]
    else:
        sorted_model_names = sorted_model_names[:n_select]
    
    model_store_final = []

    logger.info("Finalizing top_n models")

    logger.info("SubProcess create_model() called ==================================")
    for i in sorted_model_names:
        monitor.iloc[2,1:] = i
        if verbose:
            if html_param:
                update_display(monitor, display_id = 'monitor')
        progress.value += 1
        k = model_dict.get(i)
        m = create_model(estimator=k, verbose = False, system=False, cross_validation=True)
        model_store_final.append(m)
    logger.info("SubProcess create_model() end ==================================")

    if len(model_store_final) == 1:
        model_store_final = model_store_final[0]

    clear_output()

    if verbose:
        if html_param:
            display(compare_models_)
        else:
            print(compare_models_.data)
    
    pd.reset_option("display.max_columns")
    
    #store in display container
    display_container.append(compare_models_.data)

    logger.info("create_model_container: " + str(len(create_model_container)))
    logger.info("master_model_container: " + str(len(master_model_container)))
    logger.info("display_container: " + str(len(display_container)))

    logger.info(str(model_store_final))
    logger.info("compare_models() succesfully completed......................................")

    return model_store_final

def create_model(estimator = None, 
                 ensemble = False, 
                 method = None, 
                 fold = 10, 
                 round = 4,
                 cross_validation = True, #added in pycaret==2.0.0
                 verbose = True,
                 system = True, #added in pycaret==2.0.0
                 **kwargs): #added in pycaret==2.0.0
    
     
    """
    This function creates a model and scores it using Kfold Cross Validation. 
    The output prints a score grid that shows MAE, MSE, RMSE, RMSLE, R2 and 
    MAPE by fold (default = 10 Fold).

    This function returns a trained model object. 

    setup() function must be called before using create_model()

    Example
    -------
    >>> from pycaret.datasets import get_data
    >>> boston = get_data('boston')
    >>> experiment_name = setup(data = boston,  target = 'medv')
    
    >>> lr = create_model('lr')

    This will create a trained Linear Regression model.

    Parameters
    ----------
    estimator : string / object, default = None
        Enter ID of the estimators available in model library or pass an untrained model 
        object consistent with fit / predict API to train and evaluate model. All estimators 
        support binary or multiclass problem. List of estimators in model library (ID - Name):

        * 'lr' - Linear Regression                   
        * 'lasso' - Lasso Regression                
        * 'ridge' - Ridge Regression                
        * 'en' - Elastic Net                   
        * 'lar' - Least Angle Regression                  
        * 'llar' - Lasso Least Angle Regression                   
        * 'omp' - Orthogonal Matching Pursuit                     
        * 'br' - Bayesian Ridge                   
        * 'ard' - Automatic Relevance Determination                  
        * 'par' - Passive Aggressive Regressor                    
        * 'ransac' - Random Sample Consensus       
        * 'tr' - TheilSen Regressor                   
        * 'huber' - Huber Regressor                               
        * 'kr' - Kernel Ridge                                     
        * 'svm' - Support Vector Machine                           
        * 'knn' - K Neighbors Regressor                           
        * 'dt' - Decision Tree                                    
        * 'rf' - Random Forest                                    
        * 'et' - Extra Trees Regressor                            
        * 'ada' - AdaBoost Regressor                              
        * 'gbr' - Gradient Boosting Regressor                               
        * 'mlp' - Multi Level Perceptron                          
        * 'xgboost' - Extreme Gradient Boosting                   
        * 'lightgbm' - Light Gradient Boosting                    
        * 'catboost' - CatBoost Regressor                         

    ensemble: Boolean, default = False
        True would result in an ensemble of estimator using the method parameter defined. 

    method: String, 'Bagging' or 'Boosting', default = None.
        method must be defined when ensemble is set to True. Default method is set to None. 

    fold: integer, default = 10
        Number of folds to be used in Kfold CV. Must be at least 2. 

    round: integer, default = 4
        Number of decimal places the metrics in the score grid will be rounded to. 

    cross_validation: bool, default = True
        When cross_validation set to False fold parameter is ignored and model is trained
        on entire training dataset. No metric evaluation is returned. 

    verbose: Boolean, default = True
        Score grid is not printed when verbose is set to False.
    
    system: Boolean, default = True
        Must remain True all times. Only to be changed by internal functions.
    
    **kwargs: 
        Additional keyword arguments to pass to the estimator.

    Returns
    -------
    score_grid
        A table containing the scores of the model across the kfolds. 
        Scoring metrics used are MAE, MSE, RMSE, RMSLE, R2 and MAPE. 
        Mean and standard deviation of the scores across the folds are 
        also returned.

    model
        Trained model object.
  
    """


    '''
    
    ERROR HANDLING STARTS HERE
    
    '''
    
    import logging

    try:
        hasattr(logger, 'name')
    except:
        logger = logging.getLogger('logs')
        logger.setLevel(logging.DEBUG)
        
        # create console handler and set level to debug
        if logger.hasHandlers():
            logger.handlers.clear()
        
        ch = logging.FileHandler('logs.log')
        ch.setLevel(logging.DEBUG)

        # create formatter
        formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        logger.addHandler(ch)

    logger.info("Initializing create_model()")
    logger.info("""create_model(estimator={}, ensemble={}, method={}, fold={}, round={}, cross_validation={}, verbose={}, system={})""".\
        format(str(estimator), str(ensemble), str(method), str(fold), str(round), str(cross_validation), str(verbose), str(system)))

    logger.info("Checking exceptions")

    #exception checking   
    import sys
    
    #run_time
    import datetime, time
    runtime_start = time.time()

    #checking error for estimator (string)
    available_estimators = ['lr', 'lasso', 'ridge', 'en', 'lar', 'llar', 'omp', 'br', 'ard', 'par', 
                            'ransac', 'tr', 'huber', 'kr', 'svm', 'knn', 'dt', 'rf', 'et', 'ada', 'gbr', 
                            'mlp', 'xgboost', 'lightgbm', 'catboost']
    
    #only raise exception of estimator is of type string.
    if type(estimator) is str:
        if estimator not in available_estimators:
            sys.exit('(Value Error): Estimator Not Available. Please see docstring for list of available estimators.')
        
    #checking error for ensemble:
    if type(ensemble) is not bool:
        sys.exit('(Type Error): Ensemble parameter can only take argument as True or False.') 
    
    #checking error for method:
    
    #1 Check When method given and ensemble is not set to True.
    if ensemble is False and method is not None:
        sys.exit('(Type Error): Method parameter only accepts value when ensemble is set to True.')

    #2 Check when ensemble is set to True and method is not passed.
    if ensemble is True and method is None:
        sys.exit("(Type Error): Method parameter missing. Pass method = 'Bagging' or 'Boosting'.")
        
    #3 Check when ensemble is set to True and method is passed but not allowed.
    available_method = ['Bagging', 'Boosting']
    if ensemble is True and method not in available_method:
        sys.exit("(Value Error): Method parameter only accepts two values 'Bagging' or 'Boosting'.")
        
    #checking fold parameter
    if type(fold) is not int:
        sys.exit('(Type Error): Fold parameter only accepts integer value.')
    
    #checking round parameter
    if type(round) is not int:
        sys.exit('(Type Error): Round parameter only accepts integer value.')
 
    #checking verbose parameter
    if type(verbose) is not bool:
        sys.exit('(Type Error): Verbose parameter can only take argument as True or False.') 
    
    #checking system parameter
    if type(system) is not bool:
        sys.exit('(Type Error): System parameter can only take argument as True or False.') 

    #checking cross_validation parameter
    if type(cross_validation) is not bool:
        sys.exit('(Type Error): cross_validation parameter can only take argument as True or False.') 
    
    '''
    
    ERROR HANDLING ENDS HERE
    
    '''
    
    logger.info("Preloading libraries")

    #pre-load libraries
    import pandas as pd
    import ipywidgets as ipw
    from IPython.display import display, HTML, clear_output, update_display
    import datetime, time
    
    logger.info("Preparing display monitor")
    
    #progress bar
    progress = ipw.IntProgress(value=0, min=0, max=fold+4, step=1 , description='Processing: ')
    master_display = pd.DataFrame(columns=['MAE','MSE','RMSE', 'R2', 'RMSLE', 'MAPE'])
    if verbose:
        if html_param:
            display(progress)
    
    #display monitor
    timestampStr = datetime.datetime.now().strftime("%H:%M:%S")
    monitor = pd.DataFrame( [ ['Initiated' , '. . . . . . . . . . . . . . . . . .', timestampStr ], 
                             ['Status' , '. . . . . . . . . . . . . . . . . .' , 'Loading Dependencies' ],
                             ['ETC' , '. . . . . . . . . . . . . . . . . .',  'Calculating ETC'] ],
                              columns=['', ' ', '   ']).set_index('')
    
    if verbose:
        if html_param:
            display(monitor, display_id = 'monitor')
            display_ = display(master_display, display_id=True)
            display_id = display_.display_id
    
    #ignore warnings
    import warnings
    warnings.filterwarnings('ignore') 

    logger.info("Copying training dataset")

    #Storing X_train and y_train in data_X and data_y parameter
    data_X = X_train.copy()
    data_y = y_train.copy()
    
    #reset index
    data_X.reset_index(drop=True, inplace=True)
    data_y.reset_index(drop=True, inplace=True)

    logger.info("Importing libraries")
 
    #general dependencies
    import numpy as np
    from sklearn import metrics
    from sklearn.model_selection import KFold
    
    progress.value += 1
    
    logger.info("Defining folds")

    #cross validation setup starts here
    kf = KFold(fold, random_state=seed, shuffle=folds_shuffle_param)
    
    logger.info("Declaring metric variables")

    score_mae =np.empty((0,0))
    score_mse =np.empty((0,0))
    score_rmse =np.empty((0,0))
    score_rmsle =np.empty((0,0))
    score_r2 =np.empty((0,0))
    score_mape =np.empty((0,0))
    score_training_time=np.empty((0,0))
    avgs_mae =np.empty((0,0))
    avgs_mse =np.empty((0,0))
    avgs_rmse =np.empty((0,0))
    avgs_r2 =np.empty((0,0))
    avgs_mape =np.empty((0,0)) 
    avgs_rmsle =np.empty((0,0))
    avgs_training_time=np.empty((0,0))
    
    def calculate_mape(actual, prediction):
        mask = actual != 0
        return (np.fabs(actual - prediction)/actual)[mask].mean()
  
    '''
    MONITOR UPDATE STARTS
    '''
    
    monitor.iloc[1,1:] = 'Selecting Estimator'
    if verbose:
        if html_param:
            update_display(monitor, display_id = 'monitor')
    
    '''
    MONITOR UPDATE ENDS
    '''
        
    if estimator == 'lr':
        
        from sklearn.linear_model import LinearRegression
        model = LinearRegression(n_jobs=n_jobs_param, **kwargs)
        full_name = 'Linear Regression'
        
    elif estimator == 'lasso':
        
        from sklearn.linear_model import Lasso
        model = Lasso(random_state=seed, **kwargs)
        full_name = 'Lasso Regression'
        
    elif estimator == 'ridge':
        
        from sklearn.linear_model import Ridge
        model = Ridge(random_state=seed, **kwargs)
        full_name = 'Ridge Regression'
        
    elif estimator == 'en':
        
        from sklearn.linear_model import ElasticNet
        model = ElasticNet(random_state=seed, **kwargs)
        full_name = 'Elastic Net'
        
    elif estimator == 'lar':
        
        from sklearn.linear_model import Lars
        model = Lars(**kwargs)
        full_name = 'Least Angle Regression'
        
    elif estimator == 'llar':
        
        from sklearn.linear_model import LassoLars
        model = LassoLars(**kwargs)
        full_name = 'Lasso Least Angle Regression'
        
    elif estimator == 'omp':
        
        from sklearn.linear_model import OrthogonalMatchingPursuit
        model = OrthogonalMatchingPursuit(**kwargs)
        full_name = 'Orthogonal Matching Pursuit'
        
    elif estimator == 'br':
        from sklearn.linear_model import BayesianRidge
        model = BayesianRidge(**kwargs)
        full_name = 'Bayesian Ridge Regression' 
        
    elif estimator == 'ard':
        
        from sklearn.linear_model import ARDRegression
        model = ARDRegression(**kwargs)
        full_name = 'Automatic Relevance Determination'        
        
    elif estimator == 'par':
        
        from sklearn.linear_model import PassiveAggressiveRegressor
        model = PassiveAggressiveRegressor(random_state=seed, **kwargs)
        full_name = 'Passive Aggressive Regressor'    
        
    elif estimator == 'ransac':
        
        from sklearn.linear_model import RANSACRegressor
        model = RANSACRegressor(min_samples=0.5, random_state=seed, **kwargs)
        full_name = 'Random Sample Consensus'   
        
    elif estimator == 'tr':
        
        from sklearn.linear_model import TheilSenRegressor
        model = TheilSenRegressor(random_state=seed, n_jobs=n_jobs_param, **kwargs)
        full_name = 'TheilSen Regressor'     
        
    elif estimator == 'huber':
        
        from sklearn.linear_model import HuberRegressor
        model = HuberRegressor(**kwargs)
        full_name = 'Huber Regressor'   
        
    elif estimator == 'kr':
        
        from sklearn.kernel_ridge import KernelRidge
        model = KernelRidge(**kwargs)
        full_name = 'Kernel Ridge'
        
    elif estimator == 'svm':
        
        from sklearn.svm import SVR
        model = SVR(**kwargs)
        full_name = 'Support Vector Regression'  
        
    elif estimator == 'knn':
        
        from sklearn.neighbors import KNeighborsRegressor
        model = KNeighborsRegressor(n_jobs=n_jobs_param, **kwargs)
        full_name = 'Nearest Neighbors Regression' 
        
    elif estimator == 'dt':
        
        from sklearn.tree import DecisionTreeRegressor
        model = DecisionTreeRegressor(random_state=seed, **kwargs)
        full_name = 'Decision Tree'
        
    elif estimator == 'rf':
        
        from sklearn.ensemble import RandomForestRegressor
        model = RandomForestRegressor(random_state=seed, n_jobs=n_jobs_param, **kwargs)
        full_name = 'Random Forest Regressor'
        
    elif estimator == 'et':
        
        from sklearn.ensemble import ExtraTreesRegressor
        model = ExtraTreesRegressor(random_state=seed, n_jobs=n_jobs_param, **kwargs)
        full_name = 'Extra Trees Regressor'    
        
    elif estimator == 'ada':
        
        from sklearn.ensemble import AdaBoostRegressor
        model = AdaBoostRegressor(random_state=seed, **kwargs)
        full_name = 'AdaBoost Regressor'   
        
    elif estimator == 'gbr':
        
        from sklearn.ensemble import GradientBoostingRegressor
        model = GradientBoostingRegressor(random_state=seed, **kwargs)
        full_name = 'Gradient Boosting Regressor'       
        
    elif estimator == 'mlp':
        
        from sklearn.neural_network import MLPRegressor
        model = MLPRegressor(random_state=seed, **kwargs)
        full_name = 'MLP Regressor'
        
    elif estimator == 'xgboost':
        
        from xgboost import XGBRegressor
        model = XGBRegressor(random_state=seed, n_jobs=n_jobs_param, verbosity=0, **kwargs)
        full_name = 'Extreme Gradient Boosting Regressor'
        
    elif estimator == 'lightgbm':
        
        import lightgbm as lgb
        model = lgb.LGBMRegressor(random_state=seed, n_jobs=n_jobs_param, **kwargs)
        full_name = 'Light Gradient Boosting Machine'
        
    elif estimator == 'catboost':
        from catboost import CatBoostRegressor
        model = CatBoostRegressor(random_state=seed, silent = True, thread_count=n_jobs_param, **kwargs)
        full_name = 'CatBoost Regressor'
        
    else:

        logger.info("Declaring custom model")

        model = estimator
        
        def get_model_name(e):
            return str(e).split("(")[0]

        model_dict_logging = {'ExtraTreesRegressor' : 'Extra Trees Regressor',
                            'GradientBoostingRegressor' : 'Gradient Boosting Regressor', 
                            'RandomForestRegressor' : 'Random Forest',
                            'LGBMRegressor' : 'Light Gradient Boosting Machine',
                            'XGBRegressor' : 'Extreme Gradient Boosting',
                            'AdaBoostRegressor' : 'AdaBoost Regressor', 
                            'DecisionTreeRegressor' : 'Decision Tree', 
                            'Ridge' : 'Ridge Regression',
                            'TheilSenRegressor' : 'TheilSen Regressor', 
                            'BayesianRidge' : 'Bayesian Ridge',
                            'LinearRegression' : 'Linear Regression',
                            'ARDRegression' : 'Automatic Relevance Determination', 
                            'KernelRidge' : 'Kernel Ridge', 
                            'RANSACRegressor' : 'Random Sample Consensus', 
                            'HuberRegressor' : 'Huber Regressor', 
                            'Lasso' : 'Lasso Regression', 
                            'ElasticNet' : 'Elastic Net', 
                            'Lars' : 'Least Angle Regression', 
                            'OrthogonalMatchingPursuit' : 'Orthogonal Matching Pursuit', 
                            'MLPRegressor' : 'Multi Level Perceptron',
                            'KNeighborsRegressor' : 'K Neighbors Regressor',
                            'SVR' : 'Support Vector Machine',
                            'LassoLars' : 'Lasso Least Angle Regression',
                            'PassiveAggressiveRegressor' : 'Passive Aggressive Regressor',
                            'CatBoostRegressor' : 'CatBoost Regressor',
                            'BaggingRegressor' : 'Bagging Regressor'}

        mn = get_model_name(estimator)
        
        if 'catboost' in mn:
            mn = 'CatBoostRegressor'

        if mn in model_dict_logging.keys():
            full_name = model_dict_logging.get(mn)
        else:
            full_name = mn
    
    logger.info(str(full_name) + ' Imported succesfully')

    progress.value += 1
    
    #checking method when ensemble is set to True. 

    logger.info("Checking ensemble method")

    if method == 'Bagging':
        logger.info("Ensemble method set to Bagging")        
        from sklearn.ensemble import BaggingRegressor
        model = BaggingRegressor(model,bootstrap=True,n_estimators=10, random_state=seed)

    elif method == 'Boosting':
        logger.info("Ensemble method set to Boosting")                
        from sklearn.ensemble import AdaBoostRegressor
        model = AdaBoostRegressor(model, n_estimators=10, random_state=seed)
    
    
    '''
    MONITOR UPDATE STARTS
    '''
    
    if not cross_validation:
        monitor.iloc[1,1:] = 'Fitting ' + str(full_name)
    else:
        monitor.iloc[1,1:] = 'Initializing CV'
    
    if verbose:
        if html_param:
            update_display(monitor, display_id = 'monitor')
    
    '''
    MONITOR UPDATE ENDS
    '''
    
    if not cross_validation:

        logger.info("Cross validation set to False")

        logger.info("Fitting Model")
        model.fit(data_X,data_y)

        if verbose:
            clear_output()

        logger.info("create_model_container " + str(len(create_model_container)))
        logger.info("master_model_container " + str(len(master_model_container)))
        logger.info("display_container " + str(len(display_container)))

        logger.info(str(model))
        logger.info("create_models() succesfully completed......................................")
        return model
    
    fold_num = 1
    
    for train_i , test_i in kf.split(data_X,data_y):
        
        logger.info("Initializing Fold " + str(fold_num))

        t0 = time.time()
        
        '''
        MONITOR UPDATE STARTS
        '''
    
        monitor.iloc[1,1:] = 'Fitting Fold ' + str(fold_num) + ' of ' + str(fold)
        if verbose:
            if html_param:
                update_display(monitor, display_id = 'monitor')

        '''
        MONITOR UPDATE ENDS
        '''
        
        Xtrain,Xtest = data_X.iloc[train_i], data_X.iloc[test_i]
        ytrain,ytest = data_y.iloc[train_i], data_y.iloc[test_i]  
        time_start=time.time()
        logger.info("Fitting Model")
        model.fit(Xtrain,ytrain)
        logger.info("Evaluating Metrics")
        pred_ = model.predict(Xtest)
        
        try:
            pred_ = target_inverse_transformer.inverse_transform(np.array(pred_).reshape(-1,1))
            ytest = target_inverse_transformer.inverse_transform(np.array(ytest).reshape(-1,1))
            pred_ = np.nan_to_num(pred_)
            ytest = np.nan_to_num(ytest)
            
        except:
            pass
            logger.info("No inverse transformation")

        logger.info("Compiling Metrics")
        time_end=time.time()
        mae = metrics.mean_absolute_error(ytest,pred_)
        mse = metrics.mean_squared_error(ytest,pred_)
        rmse = np.sqrt(mse)
        rmsle = np.sqrt(np.mean(np.power(np.log(np.array(abs(pred_))+1) - np.log(np.array(abs(ytest))+1), 2)))
        r2 = metrics.r2_score(ytest,pred_)
        mape = calculate_mape(ytest,pred_)
        training_time=time_end-time_start
        score_mae = np.append(score_mae,mae)
        score_mse = np.append(score_mse,mse)
        score_rmse = np.append(score_rmse,rmse)
        score_rmsle = np.append(score_rmsle,rmsle)
        score_r2 =np.append(score_r2,r2)
        score_mape = np.append(score_mape,mape)
        score_training_time=np.append(score_training_time,training_time)
        progress.value += 1
        
        
        '''
        
        This section handles time calculation and is created to update_display() as code loops through 
        the fold defined.
        
        '''
        
        fold_results = pd.DataFrame({'MAE':[mae], 'MSE': [mse], 'RMSE': [rmse], 'R2': [r2],
                                     'RMSLE' : [rmsle], 'MAPE': [mape] }).round(round)
        master_display = pd.concat([master_display, fold_results],ignore_index=True)
        fold_results = []
        
        '''
        TIME CALCULATION SUB-SECTION STARTS HERE
        '''
        t1 = time.time()
        
        tt = (t1 - t0) * (fold-fold_num) / 60
        tt = np.around(tt, 2)
        
        if tt < 1:
            tt = str(np.around((tt * 60), 2))
            ETC = tt + ' Seconds Remaining'
                
        else:
            tt = str (tt)
            ETC = tt + ' Minutes Remaining'
            
        '''
        MONITOR UPDATE STARTS
        '''

        monitor.iloc[2,1:] = ETC
        if verbose:
            if html_param:
                update_display(monitor, display_id = 'monitor')

        '''
        MONITOR UPDATE ENDS
        '''
            
        fold_num += 1
        
        '''
        TIME CALCULATION ENDS HERE
        '''
        
        if verbose:
            if html_param:
                update_display(master_display, display_id = display_id)
            
        
        '''
        
        Update_display() ends here
        
        '''

    logger.info("Calculating mean and std")

    mean_mae=np.mean(score_mae)
    mean_mse=np.mean(score_mse)
    mean_rmse=np.mean(score_rmse)
    mean_rmsle=np.mean(score_rmsle)
    mean_r2=np.mean(score_r2)
    mean_mape=np.mean(score_mape)
    mean_training_time=np.mean(score_training_time)
    std_mae=np.std(score_mae)
    std_mse=np.std(score_mse)
    std_rmse=np.std(score_rmse)
    std_rmsle=np.std(score_rmsle)
    std_r2=np.std(score_r2)
    std_mape=np.std(score_mape)
    std_training_time=np.std(score_training_time)
    
    avgs_mae = np.append(avgs_mae, mean_mae)
    avgs_mae = np.append(avgs_mae, std_mae) 
    avgs_mse = np.append(avgs_mse, mean_mse)
    avgs_mse = np.append(avgs_mse, std_mse)
    avgs_rmse = np.append(avgs_rmse, mean_rmse)
    avgs_rmse = np.append(avgs_rmse, std_rmse)
    avgs_rmsle = np.append(avgs_rmsle, mean_rmsle)
    avgs_rmsle = np.append(avgs_rmsle, std_rmsle)
    avgs_r2 = np.append(avgs_r2, mean_r2)
    avgs_r2 = np.append(avgs_r2, std_r2)
    avgs_mape = np.append(avgs_mape, mean_mape)
    avgs_mape = np.append(avgs_mape, std_mape)
    avgs_training_time=np.append(avgs_training_time, mean_training_time)
    avgs_training_time=np.append(avgs_training_time, std_training_time)
    
    progress.value += 1
    
    logger.info("Creating metrics dataframe")

    model_results = pd.DataFrame({'MAE': score_mae, 'MSE': score_mse, 'RMSE' : score_rmse, 'R2' : score_r2,
                                  'RMSLE' : score_rmsle, 'MAPE' : score_mape})
    model_avgs = pd.DataFrame({'MAE': avgs_mae, 'MSE': avgs_mse, 'RMSE' : avgs_rmse, 'R2' : avgs_r2,
                                'RMSLE' : avgs_rmsle, 'MAPE' : avgs_mape},index=['Mean', 'SD'])

    model_results = model_results.append(model_avgs)
    model_results = model_results.round(round)
    
    #Yellow the mean
    model_results=model_results.style.apply(lambda x: ['background: yellow' if (x.name == 'Mean') else '' for i in x], axis=1)
    model_results = model_results.set_precision(round)

    #refitting the model on complete X_train, y_train
    monitor.iloc[1,1:] = 'Finalizing Model'
    monitor.iloc[2,1:] = 'Almost Finished'
    if verbose:
        if html_param:
            update_display(monitor, display_id = 'monitor')
    
    model_fit_start = time.time()
    logger.info("Finalizing model")
    model.fit(data_X, data_y)
    model_fit_end = time.time()

    model_fit_time = np.array(model_fit_end - model_fit_start).round(2)
    
    #end runtime
    runtime_end = time.time()
    runtime = np.array(runtime_end - runtime_start).round(2)

    progress.value += 1
    
    #mlflow logging
    if logging_param and system:
        
        logger.info("Creating MLFlow logs")

        #Creating Logs message monitor
        monitor.iloc[1,1:] = 'Creating Logs'
        monitor.iloc[2,1:] = 'Almost Finished'    
        if verbose:
            if html_param:
                update_display(monitor, display_id = 'monitor')

        #import mlflow
        import mlflow
        from pathlib import Path
        import os

        mlflow.set_experiment(exp_name_log)

        with mlflow.start_run(run_name=full_name) as run:

            # Get active run to log as tag
            RunID = mlflow.active_run().info.run_id

            # Log model parameters
            params = model.get_params()

            for i in list(params):
                v = params.get(i)
                if len(str(v)) > 250:
                    params.pop(i)

            mlflow.log_params(params)
            
            # Log metrics
            mlflow.log_metrics({"MAE": avgs_mae[0], "MSE": avgs_mse[0], "RMSE": avgs_rmse[0], "R2" : avgs_r2[0],
                                "RMSLE": avgs_rmsle[0], "MAPE": avgs_mape[0]})
            
            #set tag of compare_models
            mlflow.set_tag("Source", "create_model")
            
            import secrets
            URI = secrets.token_hex(nbytes=4)
            mlflow.set_tag("URI", URI)   
            mlflow.set_tag("USI", USI)
            mlflow.set_tag("Run Time", runtime)
            mlflow.set_tag("Run ID", RunID)

            # Log training time in seconds
            mlflow.log_metric("TT", model_fit_time)

            # Log the CV results as model_results.html artifact
            model_results.data.to_html('Results.html', col_space=65, justify='left')
            mlflow.log_artifact('Results.html')
            os.remove('Results.html')

            # Generate hold-out predictions and save as html
            holdout = predict_model(model, verbose=False)
            holdout_score = pull()
            del(holdout)
            display_container.pop(-1)
            holdout_score.to_html('Holdout.html', col_space=65, justify='left')
            mlflow.log_artifact('Holdout.html')
            os.remove('Holdout.html')

            # Log AUC and Confusion Matrix plot
            if log_plots_param:

                logger.info("SubProcess plot_model() called ==================================")

                try:
                    plot_model(model, plot = 'residuals', verbose=False, save=True, system=False)
                    mlflow.log_artifact('Residuals.png')
                    os.remove("Residuals.png")
                except:
                    pass

                try:
                    plot_model(model, plot = 'error', verbose=False, save=True, system=False)
                    mlflow.log_artifact('Prediction Error.png')
                    os.remove("Prediction Error.png")
                except:
                    pass

                try:
                    plot_model(model, plot = 'feature', verbose=False, save=True, system=False)
                    mlflow.log_artifact('Feature Importance.png')
                    os.remove("Feature Importance.png")
                except:
                    pass

                logger.info("SubProcess plot_model() end ==================================")

            # Log model and transformation pipeline
            from copy import deepcopy

            # get default conda env
            from mlflow.sklearn import get_default_conda_env
            default_conda_env = get_default_conda_env()
            default_conda_env['name'] = str(exp_name_log) + '-env'
            default_conda_env.get('dependencies').pop(-3)
            dependencies = default_conda_env.get('dependencies')[-1]
            from pycaret.utils import __version__
            dep = 'pycaret==' + str(__version__())
            dependencies['pip'] = [dep]
            
            # define model signature
            from mlflow.models.signature import infer_signature
            signature = infer_signature(data_before_preprocess.drop([target_param], axis=1))
            input_example = data_before_preprocess.drop([target_param], axis=1).iloc[0].to_dict()

            # log model as sklearn flavor
            prep_pipe_temp = deepcopy(prep_pipe)
            prep_pipe_temp.steps.append(['trained model', model])
            mlflow.sklearn.log_model(prep_pipe_temp, "model", conda_env = default_conda_env, signature = signature, input_example = input_example)
            del(prep_pipe_temp)

    progress.value += 1

    logger.info("Uploading results into container")    
    #storing results in create_model_container
    create_model_container.append(model_results.data)
    display_container.append(model_results.data)
    
    #storing results in master_model_container
    logger.info("Uploading model into container")
    master_model_container.append(model)

    if verbose:
        clear_output()

        if html_param:
            display(model_results)
        else:
            print(model_results.data)

    logger.info("create_model_container: " + str(len(create_model_container)))
    logger.info("master_model_container: " + str(len(master_model_container)))
    logger.info("display_container: " + str(len(display_container)))

    logger.info(str(model))
    logger.info("create_model() succesfully completed......................................")
    return model

def tune_model(estimator, 
               fold = 10, 
               round = 4, 
               n_iter = 10,
               custom_grid = None, #added in pycaret==2.0.0 
               optimize = 'R2',
               choose_better = False, #added in pycaret==2.0.0
               verbose = True):
    
      
    """
    This function tunes the hyperparameters of a model and scores it using Kfold 
    Cross Validation. The output prints the score grid that shows MAE, MSE, RMSE, 
    R2, RMSLE and MAPE by fold (by default = 10 Folds).

    This function returns a trained model object.  

    tune_model() only accepts a string parameter for estimator.

    Example
    -------
    >>> from pycaret.datasets import get_data
    >>> boston = get_data('boston')
    >>> experiment_name = setup(data = boston,  target = 'medv')
    >>> xgboost = create_model('xgboost')
    >>> tuned_xgboost = tune_model(xgboost) 

    This will tune the hyperparameters of Extreme Gradient Boosting Regressor.

    Parameters
    ----------
    estimator : object, default = None

    fold: integer, default = 10
        Number of folds to be used in Kfold CV. Must be at least 2. 

    round: integer, default = 4
        Number of decimal places the metrics in the score grid will be rounded to. 

    n_iter: integer, default = 10
        Number of iterations within the Random Grid Search. For every iteration, 
        the model randomly selects one value from the pre-defined grid of hyperparameters.

    custom_grid: dictionary, default = None
        To use custom hyperparameters for tuning pass a dictionary with parameter name
        and values to be iterated. When set to None it uses pre-defined tuning grid.  

    optimize: string, default = 'R2'
        Measure used to select the best model through hyperparameter tuning.
        The default scoring measure is 'R2'. Other measures include 'MAE', 'MSE', 'RMSE',
        'RMSLE', 'MAPE'. When using 'RMSE' or 'RMSLE' the base scorer is 'MSE' and when using
        'MAPE' the base scorer is 'MAE'.

    choose_better: Boolean, default = False
        When set to set to True, base estimator is returned when the metric doesn't improve 
        by tune_model. This gurantees the returned object would perform atleast equivalent 
        to base estimator created using create_model or model returned by compare_models.

    verbose: Boolean, default = True
        Score grid is not printed when verbose is set to False.

    Returns
    -------
    score_grid
        A table containing the scores of the model across the kfolds. 
        Scoring metrics used are MAE, MSE, RMSE, R2, RMSLE and MAPE.
        Mean and standard deviation of the scores across the folds are 
        also returned.

    model
        trained model object

    Warnings
    --------
    - estimator parameter takes an abbreviated string. Passing a trained model object
      returns an error. The tune_model() function internally calls create_model() 
      before tuning the hyperparameters.
        
         
  """
 


    '''
    
    ERROR HANDLING STARTS HERE
    
    '''
    
    import logging

    try:
        hasattr(logger, 'name')
    except:
        logger = logging.getLogger('logs')
        logger.setLevel(logging.DEBUG)
        
        # create console handler and set level to debug
        if logger.hasHandlers():
            logger.handlers.clear()
        
        ch = logging.FileHandler('logs.log')
        ch.setLevel(logging.DEBUG)

        # create formatter
        formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        logger.addHandler(ch)

    logger.info("Initializing tune_model()")
    logger.info("""tune_model(estimator={}, fold={}, round={}, n_iter={}, custom_grid={}, optimize={}, choose_better={}, verbose={})""".\
        format(str(estimator), str(fold), str(round), str(n_iter), str(custom_grid), str(optimize), str(choose_better), str(verbose)))

    logger.info("Checking exceptions")

    #exception checking   
    import sys
    
    #run_time
    import datetime, time
    runtime_start = time.time()

    #checking estimator if string
    if type(estimator) is str:
        sys.exit('(Type Error): The behavior of tune_model in version 1.0.1 is changed. Please pass trained model object.') 
        
    #checking fold parameter
    if type(fold) is not int:
        sys.exit('(Type Error): Fold parameter only accepts integer value.')
    
    #checking round parameter
    if type(round) is not int:
        sys.exit('(Type Error): Round parameter only accepts integer value.')
 
    #checking n_iter parameter
    if type(n_iter) is not int:
        sys.exit('(Type Error): n_iter parameter only accepts integer value.')

    #checking optimize parameter
    allowed_optimize = ['MAE', 'MSE', 'R2', 'RMSE', 'RMSLE', 'MAPE']
    if optimize not in allowed_optimize:
        sys.exit('(Value Error): Optimization method not supported. See docstring for list of available parameters.')
    
    if type(n_iter) is not int:
        sys.exit('(Type Error): n_iter parameter only accepts integer value.')
        
    #checking verbose parameter
    if type(verbose) is not bool:
        sys.exit('(Type Error): Verbose parameter can only take argument as True or False.') 
    
    
    '''
    
    ERROR HANDLING ENDS HERE
    
    '''
    
    logger.info("Preloading libraries")

    #pre-load libraries
    import pandas as pd
    import time, datetime
    import ipywidgets as ipw
    from IPython.display import display, HTML, clear_output, update_display
    
    logger.info("Preparing display monitor")

    #progress bar
    progress = ipw.IntProgress(value=0, min=0, max=fold+6, step=1 , description='Processing: ')
    master_display = pd.DataFrame(columns=['MAE','MSE','RMSE', 'R2', 'RMSLE', 'MAPE'])
    if verbose:
        if html_param:
            display(progress)    
    
    #display monitor
    timestampStr = datetime.datetime.now().strftime("%H:%M:%S")
    monitor = pd.DataFrame( [ ['Initiated' , '. . . . . . . . . . . . . . . . . .', timestampStr ], 
                             ['Status' , '. . . . . . . . . . . . . . . . . .' , 'Loading Dependencies' ],
                             ['ETC' , '. . . . . . . . . . . . . . . . . .',  'Calculating ETC'] ],
                              columns=['', ' ', '   ']).set_index('')
    
    if verbose:
        if html_param:
            display(monitor, display_id = 'monitor')
    
    if verbose:
        if html_param:
            display_ = display(master_display, display_id=True)
            display_id = display_.display_id
    
    #ignore warnings
    import warnings
    warnings.filterwarnings('ignore') 
    
    #ignore warnings
    import warnings
    warnings.filterwarnings('ignore')    

    logger.info("Copying training dataset")

    #Storing X_train and y_train in data_X and data_y parameter
    data_X = X_train.copy()
    data_y = y_train.copy()
    
    #reset index
    data_X.reset_index(drop=True, inplace=True)
    data_y.reset_index(drop=True, inplace=True)

    logger.info("Importing libraries")    
    #general dependencies
    import random
    import numpy as np
    from sklearn import metrics
    from sklearn.model_selection import KFold
    from sklearn.model_selection import RandomizedSearchCV

    #setting numpy seed
    np.random.seed(seed)

    #define optimizer
    if optimize == 'MAE':
        optimize = 'neg_mean_absolute_error'
        compare_dimension = 'MAE' 
    elif optimize == 'MSE':
        optimize = 'neg_mean_squared_error'
        compare_dimension = 'MSE' 
    elif optimize == 'R2':
        optimize = 'r2'
        compare_dimension = 'R2'
    elif optimize == 'MAPE':
        optimize = 'neg_mean_absolute_error' #because mape not present in sklearn
        compare_dimension = 'MAPE'
    elif optimize == 'RMSE':
        optimize = 'neg_mean_squared_error' #because rmse not present in sklearn
        compare_dimension = 'RMSE' 
    elif optimize == 'RMSLE':
        optimize = 'neg_mean_squared_error' #because rmsle not present in sklearn
        compare_dimension = 'RMSLE' 
    
    progress.value += 1

    #convert trained estimator into string name for grids
    
    logger.info("Checking base model")

    def get_model_name(e):
        return str(e).split("(")[0]

    mn = get_model_name(estimator)

    if 'catboost' in mn:
        mn = 'CatBoostRegressor'
    
    model_dict = {'ExtraTreesRegressor' : 'et',
                'GradientBoostingRegressor' : 'gbr', 
                'RandomForestRegressor' : 'rf',
                'LGBMRegressor' : 'lightgbm',
                'XGBRegressor' : 'xgboost',
                'AdaBoostRegressor' : 'ada', 
                'DecisionTreeRegressor' : 'dt', 
                'Ridge' : 'ridge',
                'TheilSenRegressor' : 'tr', 
                'BayesianRidge' : 'br',
                'LinearRegression' : 'lr',
                'ARDRegression' : 'ard', 
                'KernelRidge' : 'kr', 
                'RANSACRegressor' : 'ransac', 
                'HuberRegressor' : 'huber', 
                'Lasso' : 'lasso', 
                'ElasticNet' : 'en', 
                'Lars' : 'lar', 
                'OrthogonalMatchingPursuit' : 'omp', 
                'MLPRegressor' : 'mlp',
                'KNeighborsRegressor' : 'knn',
                'SVR' : 'svm',
                'LassoLars' : 'llar',
                'PassiveAggressiveRegressor' : 'par',
                'CatBoostRegressor' : 'catboost',
                'BaggingRegressor' : 'Bagging'}

    model_dict_logging = {'ExtraTreesRegressor' : 'Extra Trees Regressor',
                        'GradientBoostingRegressor' : 'Gradient Boosting Regressor', 
                        'RandomForestRegressor' : 'Random Forest',
                        'LGBMRegressor' : 'Light Gradient Boosting Machine',
                        'XGBRegressor' : 'Extreme Gradient Boosting',
                        'AdaBoostRegressor' : 'AdaBoost Regressor', 
                        'DecisionTreeRegressor' : 'Decision Tree', 
                        'Ridge' : 'Ridge Regression',
                        'TheilSenRegressor' : 'TheilSen Regressor', 
                        'BayesianRidge' : 'Bayesian Ridge',
                        'LinearRegression' : 'Linear Regression',
                        'ARDRegression' : 'Automatic Relevance Determination', 
                        'KernelRidge' : 'Kernel Ridge', 
                        'RANSACRegressor' : 'Random Sample Consensus', 
                        'HuberRegressor' : 'Huber Regressor', 
                        'Lasso' : 'Lasso Regression', 
                        'ElasticNet' : 'Elastic Net', 
                        'Lars' : 'Least Angle Regression', 
                        'OrthogonalMatchingPursuit' : 'Orthogonal Matching Pursuit', 
                        'MLPRegressor' : 'Multi Level Perceptron',
                        'KNeighborsRegressor' : 'K Neighbors Regressor',
                        'SVR' : 'Support Vector Machine',
                        'LassoLars' : 'Lasso Least Angle Regression',
                        'PassiveAggressiveRegressor' : 'Passive Aggressive Regressor',
                        'CatBoostRegressor' : 'CatBoost Regressor',
                        'BaggingRegressor' : 'Bagging Regressor'}

    _estimator_ = estimator

    estimator = model_dict.get(mn)

    logger.info('Base model : ' + str(model_dict_logging.get(mn)))

    progress.value += 1
    
    logger.info("Defining folds")
    kf = KFold(fold, random_state=seed, shuffle=folds_shuffle_param)

    logger.info("Declaring metric variables")
    score_mae =np.empty((0,0))
    score_mse =np.empty((0,0))
    score_rmse =np.empty((0,0))
    score_rmsle =np.empty((0,0))
    score_r2 =np.empty((0,0))
    score_mape =np.empty((0,0))
    score_training_time=np.empty((0,0))
    avgs_mae =np.empty((0,0))
    avgs_mse =np.empty((0,0))
    avgs_rmse =np.empty((0,0))
    avgs_rmsle =np.empty((0,0))
    avgs_r2 =np.empty((0,0))
    avgs_mape =np.empty((0,0))
    avgs_training_time=np.empty((0,0))
    
    def calculate_mape(actual, prediction):
        mask = actual != 0
        return (np.fabs(actual - prediction)/actual)[mask].mean()
    
    '''
    MONITOR UPDATE STARTS
    '''
    
    monitor.iloc[1,1:] = 'Searching Hyperparameters'
    if verbose:
        if html_param:
            update_display(monitor, display_id = 'monitor')
    
    '''
    MONITOR UPDATE ENDS
    '''
    
    logger.info("Defining Hyperparameters")
    logger.info("Initializing RandomizedSearchCV")

    #setting turbo parameters
    cv = 3
    
    if estimator == 'lr':
        
        from sklearn.linear_model import LinearRegression

        if custom_grid is not None:
            param_grid = custom_grid
        else:
            param_grid = {'fit_intercept': [True, False],
                        'normalize' : [True, False]
                        }        
        model_grid = RandomizedSearchCV(estimator=LinearRegression(n_jobs=n_jobs_param), param_distributions=param_grid, 
                                        scoring=optimize, n_iter=n_iter, cv=cv, random_state=seed,
                                        n_jobs=n_jobs_param, iid=False)

        model_grid.fit(X_train,y_train)
        model = model_grid.best_estimator_
        best_model = model_grid.best_estimator_
        best_model_param = model_grid.best_params_

    elif estimator == 'lasso':

        from sklearn.linear_model import Lasso

        if custom_grid is not None:
            param_grid = custom_grid
        else:
            param_grid = {'alpha': np.arange(0,1,0.001),
                        'fit_intercept': [True, False],
                        'normalize' : [True, False],
                        }
        model_grid = RandomizedSearchCV(estimator=Lasso(random_state=seed), 
                                        param_distributions=param_grid, scoring=optimize, n_iter=n_iter, cv=cv, 
                                        random_state=seed, iid=False,n_jobs=n_jobs_param)
        
        model_grid.fit(X_train,y_train)
        model = model_grid.best_estimator_
        best_model = model_grid.best_estimator_
        best_model_param = model_grid.best_params_

    elif estimator == 'ridge':

        from sklearn.linear_model import Ridge

        if custom_grid is not None:
            param_grid = custom_grid
        else:
            param_grid = {"alpha": np.arange(0,1,0.001),
                        "fit_intercept": [True, False],
                        "normalize": [True, False],
                        }

        model_grid = RandomizedSearchCV(estimator=Ridge(random_state=seed), param_distributions=param_grid,
                                       scoring=optimize, n_iter=n_iter, cv=cv, random_state=seed,
                                       iid=False, n_jobs=n_jobs_param)

        model_grid.fit(X_train,y_train)
        model = model_grid.best_estimator_
        best_model = model_grid.best_estimator_
        best_model_param = model_grid.best_params_

    elif estimator == 'en':

        from sklearn.linear_model import ElasticNet

        if custom_grid is not None:
            param_grid = custom_grid
        else:
            param_grid = {'alpha': np.arange(0,1,0.01), 
                        'l1_ratio' : np.arange(0,1,0.01),
                        'fit_intercept': [True, False],
                        'normalize': [True, False]
                        } 

        model_grid = RandomizedSearchCV(estimator=ElasticNet(random_state=seed), 
                                        param_distributions=param_grid, scoring=optimize, n_iter=n_iter, cv=cv, 
                                        random_state=seed, iid=False, n_jobs=n_jobs_param)

        model_grid.fit(X_train,y_train)
        model = model_grid.best_estimator_
        best_model = model_grid.best_estimator_
        best_model_param = model_grid.best_params_

    elif estimator == 'lar':

        from sklearn.linear_model import Lars

        if custom_grid is not None:
            param_grid = custom_grid
        else:
            param_grid = {'fit_intercept':[True, False],
                        'normalize' : [True, False],
                        'eps': [0.00001, 0.0001, 0.001, 0.01, 0.05, 0.0005, 0.005, 0.00005, 0.02, 0.007]}

        model_grid = RandomizedSearchCV(estimator=Lars(), param_distributions=param_grid,
                                       scoring=optimize, n_iter=n_iter, cv=cv, random_state=seed,
                                       n_jobs=n_jobs_param)

        model_grid.fit(X_train,y_train)
        model = model_grid.best_estimator_
        best_model = model_grid.best_estimator_
        best_model_param = model_grid.best_params_  

    elif estimator == 'llar':

        from sklearn.linear_model import LassoLars

        if custom_grid is not None:
            param_grid = custom_grid
        else:
            param_grid = {'alpha': [0.0001,0.001,0.1,0.15,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9],
                        'fit_intercept':[True, False],
                        'normalize' : [True, False],
                        'eps': [0.00001, 0.0001, 0.001, 0.01, 0.05, 0.0005, 0.005, 0.00005, 0.02, 0.007]}

        model_grid = RandomizedSearchCV(estimator=LassoLars(), param_distributions=param_grid,
                                       scoring=optimize, n_iter=n_iter, cv=cv, random_state=seed,
                                       n_jobs=n_jobs_param)

        model_grid.fit(X_train,y_train)
        model = model_grid.best_estimator_
        best_model = model_grid.best_estimator_
        best_model_param = model_grid.best_params_    

    elif estimator == 'omp':

        from sklearn.linear_model import OrthogonalMatchingPursuit
        import random

        if custom_grid is not None:
            param_grid = custom_grid

        else:
            param_grid = {'n_nonzero_coefs': range(1, len(X_train.columns)+1),
                        'fit_intercept' : [True, False],
                        'normalize': [True, False]}

        model_grid = RandomizedSearchCV(estimator=OrthogonalMatchingPursuit(), 
                                        param_distributions=param_grid, scoring=optimize, n_iter=n_iter, 
                                        cv=cv, random_state=seed, n_jobs=n_jobs_param)

        model_grid.fit(X_train,y_train)
        model = model_grid.best_estimator_
        best_model = model_grid.best_estimator_
        best_model_param = model_grid.best_params_        

    elif estimator == 'br':

        from sklearn.linear_model import BayesianRidge

        if custom_grid is not None:
            param_grid = custom_grid

        else:

            param_grid = {'alpha_1': [0.0000001, 0.000001, 0.0001, 0.001, 0.01, 0.0005, 0.005, 0.05, 0.1, 0.15, 0.2, 0.3],
                        'alpha_2': [0.0000001, 0.000001, 0.0001, 0.001, 0.01, 0.0005, 0.005, 0.05, 0.1, 0.15, 0.2, 0.3],
                        'lambda_1': [0.0000001, 0.000001, 0.0001, 0.001, 0.01, 0.0005, 0.005, 0.05, 0.1, 0.15, 0.2, 0.3],
                        'lambda_2': [0.0000001, 0.000001, 0.0001, 0.001, 0.01, 0.0005, 0.005, 0.05, 0.1, 0.15, 0.2, 0.3],
                        'compute_score': [True, False],
                        'fit_intercept': [True, False],
                        'normalize': [True, False]
                        }    

        model_grid = RandomizedSearchCV(estimator=BayesianRidge(), 
                                        param_distributions=param_grid, scoring=optimize, n_iter=n_iter, 
                                        cv=cv, random_state=seed, n_jobs=n_jobs_param)

        model_grid.fit(X_train,y_train)
        model = model_grid.best_estimator_
        best_model = model_grid.best_estimator_
        best_model_param = model_grid.best_params_    

    elif estimator == 'ard':

        from sklearn.linear_model import ARDRegression

        if custom_grid is not None:
            param_grid = custom_grid

        else:
            param_grid = {'alpha_1': [0.0000001, 0.000001, 0.0001, 0.001, 0.01, 0.0005, 0.005, 0.05, 0.1, 0.15, 0.2, 0.3],
                        'alpha_2': [0.0000001, 0.000001, 0.0001, 0.001, 0.01, 0.0005, 0.005, 0.05, 0.1, 0.15, 0.2, 0.3],
                        'lambda_1': [0.0000001, 0.000001, 0.0001, 0.001, 0.01, 0.0005, 0.005, 0.05, 0.1, 0.15, 0.2, 0.3],
                        'lambda_2': [0.0000001, 0.000001, 0.0001, 0.001, 0.01, 0.0005, 0.005, 0.05, 0.1, 0.15, 0.2, 0.3],
                        'threshold_lambda' : [5000,10000,15000,20000,25000,30000,35000,40000,45000,50000,55000,60000],
                        'compute_score': [True, False],
                        'fit_intercept': [True, False],
                        'normalize': [True, False]
                        }    

        model_grid = RandomizedSearchCV(estimator=ARDRegression(), 
                                        param_distributions=param_grid, scoring=optimize, n_iter=n_iter, 
                                        cv=cv, random_state=seed, n_jobs=n_jobs_param)

        model_grid.fit(X_train,y_train)
        model = model_grid.best_estimator_
        best_model = model_grid.best_estimator_
        best_model_param = model_grid.best_params_       

    elif estimator == 'par':

        from sklearn.linear_model import PassiveAggressiveRegressor

        if custom_grid is not None:
            param_grid = custom_grid

        else:
            param_grid = {'C': np.arange(0,1,0.01), #[0.01, 0.005, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
                        'fit_intercept': [True, False],
                        'early_stopping' : [True, False],
                        #'validation_fraction': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
                        'loss' : ['epsilon_insensitive', 'squared_epsilon_insensitive'],
                        'epsilon' : [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
                        'shuffle' : [True, False]
                        }    

        model_grid = RandomizedSearchCV(estimator=PassiveAggressiveRegressor(random_state=seed), 
                                        param_distributions=param_grid, scoring=optimize, n_iter=n_iter, 
                                        cv=cv, random_state=seed, n_jobs=n_jobs_param)

        model_grid.fit(X_train,y_train)
        model = model_grid.best_estimator_
        best_model = model_grid.best_estimator_
        best_model_param = model_grid.best_params_         

    elif estimator == 'ransac':

        from sklearn.linear_model import RANSACRegressor

        if custom_grid is not None:
            param_grid = custom_grid

        else:

            param_grid = {'min_samples': np.arange(0,1,0.05), #[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
                        'max_trials': np.arange(1,20,1), #[1,2,3,4,5,6,7,8,9,10,11,12,13,14],
                        'max_skips': np.arange(1,20,1), #[1,2,3,4,5,6,7,8,9,10],
                        'stop_n_inliers': np.arange(1,25,1), #[1,2,3,4,5,6,7,8,9,10],
                        'stop_probability': np.arange(0,1,0.01), #[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
                        'loss' : ['absolute_loss', 'squared_loss'],
                        }    

        model_grid = RandomizedSearchCV(estimator=RANSACRegressor(random_state=seed), 
                                        param_distributions=param_grid, scoring=optimize, n_iter=n_iter, 
                                        cv=cv, random_state=seed, n_jobs=n_jobs_param)

        model_grid.fit(X_train,y_train)
        model = model_grid.best_estimator_
        best_model = model_grid.best_estimator_
        best_model_param = model_grid.best_params_         

    elif estimator == 'tr':

        from sklearn.linear_model import TheilSenRegressor

        if custom_grid is not None:
            param_grid = custom_grid

        else:

            param_grid = {'fit_intercept': [True, False],
                        'max_subpopulation': [5000, 10000, 15000, 20000, 25000, 30000, 40000, 50000]
                        }    

        model_grid = RandomizedSearchCV(estimator=TheilSenRegressor(random_state=seed, n_jobs=n_jobs_param), 
                                        param_distributions=param_grid, scoring=optimize, n_iter=n_iter, 
                                        cv=cv, random_state=seed, n_jobs=n_jobs_param)

        model_grid.fit(X_train,y_train)
        model = model_grid.best_estimator_
        best_model = model_grid.best_estimator_
        best_model_param = model_grid.best_params_    

    elif estimator == 'huber':

        from sklearn.linear_model import HuberRegressor

        if custom_grid is not None:
            param_grid = custom_grid

        else:
            param_grid = {'epsilon': [1.1, 1.2, 1.3, 1.35, 1.4, 1.5, 1.55, 1.6, 1.7, 1.8, 1.9],
                        'alpha': np.arange(0,1,0.0001), #[0.00001, 0.0001, 0.0003, 0.005, 0.05, 0.1, 0.0005, 0.15],
                        'fit_intercept' : [True, False]
                        }    

        model_grid = RandomizedSearchCV(estimator=HuberRegressor(), 
                                        param_distributions=param_grid, scoring=optimize, n_iter=n_iter, 
                                        cv=cv, random_state=seed, n_jobs=n_jobs_param)

        model_grid.fit(X_train,y_train)
        model = model_grid.best_estimator_
        best_model = model_grid.best_estimator_
        best_model_param = model_grid.best_params_        

    elif estimator == 'kr':

        from sklearn.kernel_ridge import KernelRidge

        if custom_grid is not None:
            param_grid = custom_grid

        else:
            param_grid = {'alpha': np.arange(0,1,0.01) }    

        model_grid = RandomizedSearchCV(estimator=KernelRidge(), 
                                        param_distributions=param_grid, scoring=optimize, n_iter=n_iter, 
                                        cv=cv, random_state=seed, n_jobs=n_jobs_param)

        model_grid.fit(X_train,y_train)
        model = model_grid.best_estimator_
        best_model = model_grid.best_estimator_
        best_model_param = model_grid.best_params_       

    elif estimator == 'svm':

        from sklearn.svm import SVR
        
        if custom_grid is not None:
            param_grid = custom_grid

        else:

            param_grid = {'C' : np.arange(0, 10, 0.001), 
                        'epsilon' : [1.1, 1.2, 1.3, 1.35, 1.4, 1.5, 1.55, 1.6, 1.7, 1.8, 1.9],
                        'shrinking': [True, False]
                        }    

        model_grid = RandomizedSearchCV(estimator=SVR(), 
                                        param_distributions=param_grid, scoring=optimize, n_iter=n_iter, 
                                        cv=cv, random_state=seed, n_jobs=n_jobs_param)

        model_grid.fit(X_train,y_train)
        model = model_grid.best_estimator_
        best_model = model_grid.best_estimator_
        best_model_param = model_grid.best_params_     

    elif estimator == 'knn':

        from sklearn.neighbors import KNeighborsRegressor

        if custom_grid is not None:
            param_grid = custom_grid

        else:
            param_grid = {'n_neighbors': range(1,51),
                        'weights' :  ['uniform', 'distance'],
                        'algorithm': ['ball_tree', 'kd_tree', 'brute'],
                        'leaf_size': [10,20,30,40,50,60,70,80,90]
                        } 

        model_grid = RandomizedSearchCV(estimator=KNeighborsRegressor(n_jobs=n_jobs_param), 
                                        param_distributions=param_grid, scoring=optimize, n_iter=n_iter, 
                                        cv=cv, random_state=seed, n_jobs=n_jobs_param)

        model_grid.fit(X_train,y_train)
        model = model_grid.best_estimator_
        best_model = model_grid.best_estimator_
        best_model_param = model_grid.best_params_         

    elif estimator == 'dt':

        from sklearn.tree import DecisionTreeRegressor

        if custom_grid is not None:
            param_grid = custom_grid

        else:

            param_grid = {"max_depth": np.random.randint(1, (len(X_train.columns)*.85),20),
                        "max_features": np.random.randint(1, len(X_train.columns),20),
                        "min_samples_leaf": [2,3,4,5,6],
                        "criterion": ["mse", "mae", "friedman_mse"],
                        } 

        model_grid = RandomizedSearchCV(estimator=DecisionTreeRegressor(random_state=seed), 
                                        param_distributions=param_grid, scoring=optimize, n_iter=n_iter, 
                                        cv=cv, random_state=seed, n_jobs=n_jobs_param)

        model_grid.fit(X_train,y_train)
        model = model_grid.best_estimator_
        best_model = model_grid.best_estimator_
        best_model_param = model_grid.best_params_         

    elif estimator == 'rf':

        from sklearn.ensemble import RandomForestRegressor

        if custom_grid is not None:
            param_grid = custom_grid

        else:
            param_grid = {'n_estimators': np.arange(10,300,10),
                        'criterion': ['mse', 'mae'],
                        'max_depth': [int(x) for x in np.linspace(10, 110, num = 11)],
                        'min_samples_split': [2, 5, 7, 9, 10],
                        'min_samples_leaf' : [1, 2, 4, 7, 9],
                        'max_features' : ['auto', 'sqrt', 'log2'],
                        'bootstrap': [True, False]
                        }

        model_grid = RandomizedSearchCV(estimator=RandomForestRegressor(random_state=seed, n_jobs=n_jobs_param), 
                                        param_distributions=param_grid, scoring=optimize, n_iter=n_iter, 
                                        cv=cv, random_state=seed, n_jobs=n_jobs_param)

        model_grid.fit(X_train,y_train)
        model = model_grid.best_estimator_
        best_model = model_grid.best_estimator_
        best_model_param = model_grid.best_params_       


    elif estimator == 'et':

        from sklearn.ensemble import ExtraTreesRegressor

        if custom_grid is not None:
            param_grid = custom_grid

        else:
            param_grid = {'n_estimators': np.arange(10,300,10),
                        'criterion': ['mse', 'mae'],
                        'max_depth': [int(x) for x in np.linspace(10, 110, num = 11)],
                        'min_samples_split': [2, 5, 7, 9, 10],
                        'min_samples_leaf' : [1, 2, 4, 5, 7, 9],
                        'max_features' : ['auto', 'sqrt', 'log2'],
                        'bootstrap': [True, False]
                        }  

        model_grid = RandomizedSearchCV(estimator=ExtraTreesRegressor(random_state=seed, n_jobs=n_jobs_param), 
                                        param_distributions=param_grid, scoring=optimize, n_iter=n_iter, 
                                        cv=cv, random_state=seed, n_jobs=n_jobs_param)

        model_grid.fit(X_train,y_train)
        model = model_grid.best_estimator_
        best_model = model_grid.best_estimator_
        best_model_param = model_grid.best_params_       

    elif estimator == 'ada':

        from sklearn.ensemble import AdaBoostRegressor

        if custom_grid is not None:
            param_grid = custom_grid

        else:
            param_grid = {'n_estimators': np.arange(10,200,5),
                        'learning_rate': np.arange(0.1,1,0.01),
                        'loss' : ["linear", "square", "exponential"]
                        }    

        model_grid = RandomizedSearchCV(estimator=AdaBoostRegressor(base_estimator = _estimator_.base_estimator, random_state=seed, ), 
                                        param_distributions=param_grid, scoring=optimize, n_iter=n_iter, 
                                        cv=cv, random_state=seed, n_jobs=n_jobs_param)

        model_grid.fit(X_train,y_train)
        model = model_grid.best_estimator_
        best_model = model_grid.best_estimator_
        best_model_param = model_grid.best_params_ 

    elif estimator == 'gbr':

        from sklearn.ensemble import GradientBoostingRegressor

        if custom_grid is not None:
            param_grid = custom_grid

        else:
            param_grid = {'loss': ['ls', 'lad', 'huber', 'quantile'],
                        'n_estimators': np.arange(10,200,5),
                        'learning_rate': np.arange(0,1,0.01),
                        'subsample' : [0.1,0.3,0.5,0.7,0.9,1],
                        'criterion' : ['friedman_mse', 'mse', 'mae'],
                        'min_samples_split' : [2,4,5,7,9,10],
                        'min_samples_leaf' : [1,2,3,4,5,7],
                        'max_depth': [int(x) for x in np.linspace(10, 110, num = 11)],
                        'max_features' : ['auto', 'sqrt', 'log2']
                        }     

        model_grid = RandomizedSearchCV(estimator=GradientBoostingRegressor(random_state=seed), 
                                        param_distributions=param_grid, scoring=optimize, n_iter=n_iter, 
                                        cv=cv, random_state=seed, n_jobs=n_jobs_param)

        model_grid.fit(X_train,y_train)
        model = model_grid.best_estimator_
        best_model = model_grid.best_estimator_
        best_model_param = model_grid.best_params_         

    elif estimator == 'mlp':

        from sklearn.neural_network import MLPRegressor
        
        if custom_grid is not None:
            param_grid = custom_grid

        else:
            param_grid = {'learning_rate': ['constant', 'invscaling', 'adaptive'],
                        'solver' : ['lbfgs', 'adam'],
                        'alpha': np.arange(0, 1, 0.0001), 
                        'hidden_layer_sizes': [(50,50,50), (50,100,50), (100,), (100,50,100), (100,100,100)],
                        'activation': ["tanh", "identity", "logistic","relu"]
                        }    

        model_grid = RandomizedSearchCV(estimator=MLPRegressor(random_state=seed), 
                                        param_distributions=param_grid, scoring=optimize, n_iter=n_iter, 
                                        cv=cv, random_state=seed, n_jobs=n_jobs_param)    

        model_grid.fit(X_train,y_train)
        model = model_grid.best_estimator_
        best_model = model_grid.best_estimator_
        best_model_param = model_grid.best_params_   
        
        
    elif estimator == 'xgboost':
        
        from xgboost import XGBRegressor

        if custom_grid is not None:
            param_grid = custom_grid

        else:
            param_grid = {'learning_rate': [0.01, 0.02, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1], 
                        'n_estimators':[10, 30, 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000], 
                        'subsample': [0.1, 0.2, 0.3, 0.5, 0.7, 0.9, 1],
                        'max_depth': [int(x) for x in np.linspace(10, 110, num = 11)], 
                        'colsample_bytree': [0.5, 0.7, 0.9, 1],
                        'min_child_weight': [1, 2, 3, 4]
                        }

        model_grid = RandomizedSearchCV(estimator=XGBRegressor(random_state=seed, n_jobs=n_jobs_param, verbosity=0, ), 
                                        param_distributions=param_grid, scoring=optimize, n_iter=n_iter, 
                                        cv=cv, random_state=seed, n_jobs=n_jobs_param)

        model_grid.fit(X_train,y_train)
        model = model_grid.best_estimator_
        best_model = model_grid.best_estimator_
        best_model_param = model_grid.best_params_   
        
        
    elif estimator == 'lightgbm':
        
        import lightgbm as lgb

        if custom_grid is not None:
            param_grid = custom_grid

        else:
            param_grid = {'num_leaves': [10,20,30,40,50,60,70,80,90,100,150,200],
                        'max_depth': [int(x) for x in np.linspace(10, 110, num = 11)],
                        'learning_rate': [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1],
                        'n_estimators': [10, 30, 50, 70, 90, 100, 120, 150, 170, 200], 
                        'min_split_gain' : [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9],
                        'reg_alpha': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
                        'reg_lambda': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
                        }
            
        model_grid = RandomizedSearchCV(estimator=lgb.LGBMRegressor(random_state=seed, n_jobs=n_jobs_param), 
                                        param_distributions=param_grid, scoring=optimize, n_iter=n_iter, 
                                        cv=cv, random_state=seed, n_jobs=n_jobs_param)

        model_grid.fit(X_train,y_train)
        model = model_grid.best_estimator_
        best_model = model_grid.best_estimator_
        best_model_param = model_grid.best_params_   

    elif estimator == 'catboost':
        
        from catboost import CatBoostRegressor

        if custom_grid is not None:
            param_grid = custom_grid

        else:
            param_grid = {'depth':[3,1,2,6,4,5,7,8,9,10],
                        'iterations':[250,100,500,1000], 
                        'learning_rate':[0.03,0.001,0.01,0.1,0.2,0.3], 
                        'l2_leaf_reg':[3,1,5,10,100], 
                        'border_count':[32,5,10,20,50,100,200], 
                        }
            
        model_grid = RandomizedSearchCV(estimator=CatBoostRegressor(random_state=seed, silent=True, thread_count=n_jobs_param), 
                                        param_distributions=param_grid, scoring=optimize, n_iter=n_iter, 
                                        cv=cv, random_state=seed, n_jobs=n_jobs_param)

        model_grid.fit(X_train,y_train)
        model = model_grid.best_estimator_
        best_model = model_grid.best_estimator_
        best_model_param = model_grid.best_params_ 
    
    elif estimator == 'Bagging':
        
        from sklearn.ensemble import BaggingRegressor

        if custom_grid is not None:
            param_grid = custom_grid

        else:
            param_grid = {'n_estimators': np.arange(10,300,10),
                        'bootstrap': [True, False],
                        'bootstrap_features': [True, False],
                        }
            
        model_grid = RandomizedSearchCV(estimator=BaggingRegressor(base_estimator=_estimator_.base_estimator, random_state=seed, n_jobs=n_jobs_param), 
                                        param_distributions=param_grid, scoring=optimize, n_iter=n_iter, 
                                        cv=cv, random_state=seed, n_jobs=n_jobs_param)

        model_grid.fit(X_train,y_train)
        model = model_grid.best_estimator_
        best_model = model_grid.best_estimator_
        best_model_param = model_grid.best_params_ 


    progress.value += 1
    progress.value += 1

    logger.info("Random search completed") 
    
    '''
    MONITOR UPDATE STARTS
    '''
    
    monitor.iloc[1,1:] = 'Initializing CV'
    if verbose:
        if html_param:
            update_display(monitor, display_id = 'monitor')
    
    '''
    MONITOR UPDATE ENDS
    '''
    
    fold_num = 1
    
    for train_i , test_i in kf.split(data_X,data_y):
        
        logger.info("Initializing Fold " + str(fold_num))

        t0 = time.time()
        
        
        '''
        MONITOR UPDATE STARTS
        '''
    
        monitor.iloc[1,1:] = 'Fitting Fold ' + str(fold_num) + ' of ' + str(fold)
        if verbose:
            if html_param:
                update_display(monitor, display_id = 'monitor')

        '''
        MONITOR UPDATE ENDS
        '''
        
        Xtrain,Xtest = data_X.iloc[train_i], data_X.iloc[test_i]
        ytrain,ytest = data_y.iloc[train_i], data_y.iloc[test_i]  
        time_start=time.time()
        logger.info("Fitting Model")
        model.fit(Xtrain,ytrain)
        logger.info("Evaluating Metrics")
        pred_ = model.predict(Xtest)
        
        try:
            pred_ = target_inverse_transformer.inverse_transform(np.array(pred_).reshape(-1,1))
            ytest = target_inverse_transformer.inverse_transform(np.array(ytest).reshape(-1,1))
            pred_ = np.nan_to_num(pred_)
            ytest = np.nan_to_num(ytest)
            
        except:
            pass

        logger.info("Compiling Metrics")
        time_end=time.time()
        mae = metrics.mean_absolute_error(ytest,pred_)
        mse = metrics.mean_squared_error(ytest,pred_)
        rmse = np.sqrt(mse)
        r2 = metrics.r2_score(ytest,pred_)
        rmsle = np.sqrt(np.mean(np.power(np.log(np.array(abs(pred_))+1) - np.log(np.array(abs(ytest))+1), 2)))
        mape = calculate_mape(ytest,pred_)
        training_time=time_end-time_start
        score_mae = np.append(score_mae,mae)
        score_mse = np.append(score_mse,mse)
        score_rmse = np.append(score_rmse,rmse)
        score_rmsle = np.append(score_rmsle,rmsle)
        score_r2 =np.append(score_r2,r2)
        score_mape = np.append(score_mape,mape)
        score_training_time=np.append(score_training_time,training_time)
        progress.value += 1
            
            
        '''
        
        This section is created to update_display() as code loops through the fold defined.
        
        '''
        
        fold_results = pd.DataFrame({'MAE':[mae], 'MSE': [mse], 'RMSE': [rmse], 
                                     'R2': [r2], 'RMSLE': [rmsle], 'MAPE': [mape]}).round(round)
        master_display = pd.concat([master_display, fold_results],ignore_index=True)
        fold_results = []
        
        '''
        
        TIME CALCULATION SUB-SECTION STARTS HERE
        
        '''
        
        t1 = time.time()
        
        tt = (t1 - t0) * (fold-fold_num) / 60
        tt = np.around(tt, 2)
        
        if tt < 1:
            tt = str(np.around((tt * 60), 2))
            ETC = tt + ' Seconds Remaining'
                
        else:
            tt = str (tt)
            ETC = tt + ' Minutes Remaining'
            
        if verbose:
            if html_param:
                update_display(ETC, display_id = 'ETC')
            
        fold_num += 1
        
        '''
        MONITOR UPDATE STARTS
        '''

        monitor.iloc[2,1:] = ETC
        if verbose:
            if html_param:
                update_display(monitor, display_id = 'monitor')

        '''
        MONITOR UPDATE ENDS
        '''
       
        '''
        
        TIME CALCULATION ENDS HERE
        
        '''
        
        if verbose:
            if html_param:
                update_display(master_display, display_id = display_id)
        
        '''
        
        Update_display() ends here
        
        '''
        
    progress.value += 1
    
    logger.info("Calculating mean and std")
    mean_mae=np.mean(score_mae)
    mean_mse=np.mean(score_mse)
    mean_rmse=np.mean(score_rmse)
    mean_rmsle=np.mean(score_rmsle)
    mean_r2=np.mean(score_r2)
    mean_mape=np.mean(score_mape)
    mean_training_time=np.mean(score_training_time)
    std_mae=np.std(score_mae)
    std_mse=np.std(score_mse)
    std_rmse=np.std(score_rmse)
    std_rmsle=np.std(score_rmsle)
    std_r2=np.std(score_r2)
    std_mape=np.std(score_mape)
    std_training_time=np.std(score_training_time)
    
    avgs_mae = np.append(avgs_mae, mean_mae)
    avgs_mae = np.append(avgs_mae, std_mae) 
    avgs_mse = np.append(avgs_mse, mean_mse)
    avgs_mse = np.append(avgs_mse, std_mse)
    avgs_rmse = np.append(avgs_rmse, mean_rmse)
    avgs_rmse = np.append(avgs_rmse, std_rmse)
    avgs_rmsle = np.append(avgs_rmsle, mean_rmsle)
    avgs_rmsle = np.append(avgs_rmsle, std_rmsle)
    avgs_r2 = np.append(avgs_r2, mean_r2)
    avgs_r2 = np.append(avgs_r2, std_r2)
    avgs_mape = np.append(avgs_mape, mean_mape)
    avgs_mape = np.append(avgs_mape, std_mape)
    avgs_training_time=np.append(avgs_training_time, mean_training_time)
    avgs_training_time=np.append(avgs_training_time, std_training_time)
    

    progress.value += 1
    
    logger.info("Creating metrics dataframe")
    model_results = pd.DataFrame({'MAE': score_mae, 'MSE': score_mse, 'RMSE' : score_rmse, 'R2' : score_r2,
                                  'RMSLE' : score_rmsle, 'MAPE' : score_mape})
    model_avgs = pd.DataFrame({'MAE': avgs_mae, 'MSE': avgs_mse, 'RMSE' : avgs_rmse, 'R2' : avgs_r2,
                                'RMSLE' : avgs_rmsle, 'MAPE' : avgs_mape},index=['Mean', 'SD'])

    model_results = model_results.append(model_avgs)
    model_results = model_results.round(round)
    
    # yellow the mean
    model_results=model_results.style.apply(lambda x: ['background: yellow' if (x.name == 'Mean') else '' for i in x], axis=1)
    model_results = model_results.set_precision(round)

    progress.value += 1
    
    #refitting the model on complete X_train, y_train
    monitor.iloc[1,1:] = 'Finalizing Model'
    if verbose:
        if html_param:
            update_display(monitor, display_id = 'monitor')
    
    model_fit_start = time.time()
    logger.info("Finalizing model")
    best_model.fit(data_X, data_y)
    model_fit_end = time.time()

    model_fit_time = np.array(model_fit_end - model_fit_start).round(2)
    
    progress.value += 1
    
    #storing results in create_model_container
    logger.info("Uploading results into container")
    create_model_container.append(model_results.data)
    display_container.append(model_results.data)

    #storing results in master_model_container
    logger.info("Uploading model into container")
    master_model_container.append(best_model)

    '''
    When choose_better sets to True. optimize metric in scoregrid is
    compared with base model created using create_model so that tune_model
    functions return the model with better score only. This will ensure 
    model performance is atleast equivalent to what is seen is compare_models 
    '''
    if choose_better:
        logger.info("choose_better activated")
        if verbose:
            if html_param:
                monitor.iloc[1,1:] = 'Compiling Final Results'
                monitor.iloc[2,1:] = 'Almost Finished'
                update_display(monitor, display_id = 'monitor')

        #creating base model for comparison
        logger.info("SubProcess create_model() called ==================================")
        if estimator in ['Bagging', 'ada']:
            base_model = create_model(estimator=_estimator_, verbose = False, system=False)
        else:
            base_model = create_model(estimator=estimator, verbose = False)
        base_model_results = create_model_container[-1][compare_dimension][-2:][0]
        tuned_model_results = create_model_container[-2][compare_dimension][-2:][0]
        logger.info("SubProcess create_model() end ==================================")

        if compare_dimension == 'R2':
            if tuned_model_results > base_model_results:
                best_model = best_model
            else:
                best_model = base_model
        else:
            if tuned_model_results < base_model_results:
                best_model = best_model
            else:
                best_model = base_model

        #re-instate display_constainer state 
        display_container.pop(-1)
        logger.info("choose_better completed")

    #end runtime
    runtime_end = time.time()
    runtime = np.array(runtime_end - runtime_start).round(2)
    
    #mlflow logging
    if logging_param:
        
        logger.info("Creating MLFlow logs")

        #Creating Logs message monitor
        monitor.iloc[1,1:] = 'Creating Logs'
        monitor.iloc[2,1:] = 'Almost Finished'    
        if verbose:
            if html_param:
                update_display(monitor, display_id = 'monitor')

        import mlflow
        from pathlib import Path
        import os
        
        mlflow.set_experiment(exp_name_log)
        full_name = model_dict_logging.get(mn)

        with mlflow.start_run(run_name=full_name) as run:    

            # Get active run to log as tag
            RunID = mlflow.active_run().info.run_id

            params = best_model.get_params()

            # Log model parameters
            params = model.get_params()

            for i in list(params):
                v = params.get(i)
                if len(str(v)) > 250:
                    params.pop(i)

            mlflow.log_params(params)

            mlflow.log_metrics({"MAE": avgs_mae[0], "MSE": avgs_mse[0], "RMSE": avgs_rmse[0], "R2" : avgs_r2[0],
                                "RMSLE": avgs_rmsle[0], "MAPE": avgs_mape[0]})

            #set tag of compare_models
            mlflow.set_tag("Source", "tune_model")
            
            import secrets
            URI = secrets.token_hex(nbytes=4)
            mlflow.set_tag("URI", URI)
            mlflow.set_tag("USI", USI)
            mlflow.set_tag("Run Time", runtime)
            mlflow.set_tag("Run ID", RunID)

            # Log training time in seconds
            mlflow.log_metric("TT", model_fit_time)

            # Log the CV results as model_results.html artifact
            model_results.data.to_html('Results.html', col_space=65, justify='left')
            mlflow.log_artifact('Results.html')
            os.remove('Results.html')

            # Generate hold-out predictions and save as html
            holdout = predict_model(best_model, verbose=False)
            holdout_score = pull()
            del(holdout)
            display_container.pop(-1)
            holdout_score.to_html('Holdout.html', col_space=65, justify='left')
            mlflow.log_artifact('Holdout.html')
            os.remove('Holdout.html')

            # Log AUC and Confusion Matrix plot
            if log_plots_param:

                logger.info("SubProcess plot_model() called ==================================")

                try:
                    plot_model(model, plot = 'residuals', verbose=False, save=True, system=False)
                    mlflow.log_artifact('Residuals.png')
                    os.remove("Residuals.png")
                except:
                    pass

                try:
                    plot_model(model, plot = 'error', verbose=False, save=True, system=False)
                    mlflow.log_artifact('Prediction Error.png')
                    os.remove("Prediction Error.png")
                except:
                    pass

                try:
                    plot_model(model, plot = 'feature', verbose=False, save=True, system=False)
                    mlflow.log_artifact('Feature Importance.png')
                    os.remove("Feature Importance.png")
                except:
                    pass

                logger.info("SubProcess plot_model() end ==================================")

            # Log hyperparameter tuning grid
            d1 = model_grid.cv_results_.get('params')
            dd = pd.DataFrame.from_dict(d1)
            dd['Score'] = model_grid.cv_results_.get('mean_test_score')
            dd.to_html('Iterations.html', col_space=75, justify='left')
            mlflow.log_artifact('Iterations.html')
            os.remove('Iterations.html')
    
            # Log model and transformation pipeline
            from copy import deepcopy

            # get default conda env
            from mlflow.sklearn import get_default_conda_env
            default_conda_env = get_default_conda_env()
            default_conda_env['name'] = str(exp_name_log) + '-env'
            default_conda_env.get('dependencies').pop(-3)
            dependencies = default_conda_env.get('dependencies')[-1]
            from pycaret.utils import __version__
            dep = 'pycaret==' + str(__version__())
            dependencies['pip'] = [dep]
            
            # define model signature
            from mlflow.models.signature import infer_signature
            signature = infer_signature(data_before_preprocess.drop([target_param], axis=1))
            input_example = data_before_preprocess.drop([target_param], axis=1).iloc[0].to_dict()

            # log model as sklearn flavor
            prep_pipe_temp = deepcopy(prep_pipe)
            prep_pipe_temp.steps.append(['trained model', model])
            mlflow.sklearn.log_model(prep_pipe_temp, "model", conda_env = default_conda_env, signature = signature, input_example = input_example)
            del(prep_pipe_temp)

    if verbose:
        clear_output()
        if html_param:
            display(model_results)
        else:
            print(model_results.data)
    else:
        clear_output()
    
    logger.info("create_model_container: " + str(len(create_model_container)))
    logger.info("master_model_container: " + str(len(master_model_container)))
    logger.info("display_container: " + str(len(display_container)))

    logger.info(str(best_model))
    logger.info("tune_model() succesfully completed......................................")

    return best_model

def ensemble_model(estimator,
                   method = 'Bagging', 
                   fold = 10,
                   n_estimators = 10,
                   round = 4,
                   choose_better = False, #added in pycaret==2.0.0
                   optimize = 'R2', #added in pycaret==2.0.0
                   verbose = True):
    """
    This function ensembles the trained base estimator using the method defined 
    in 'method' param (default = 'Bagging'). The output prints a score grid that 
    shows MAE, MSE, RMSE, R2, RMSLE and MAPE by fold (default CV = 10 Folds).

    This function returns a trained model object.  

    Model must be created using create_model() or tune_model().

    Example
    --------
    >>> from pycaret.datasets import get_data
    >>> boston = get_data('boston')
    >>> experiment_name = setup(data = boston,  target = 'medv')
    >>> dt = create_model('dt')
    >>> ensembled_dt = ensemble_model(dt)

    This will return an ensembled Decision Tree model using 'Bagging'.

    Parameters
    ----------
    estimator : object, default = None

    method: String, default = 'Bagging'
        Bagging method will create an ensemble meta-estimator that fits base 
        regressor each on random subsets of the original dataset. The other
        available method is 'Boosting' that fits a regressor on the original 
        dataset and then fits additional copies of the regressor on the same 
        dataset but where the weights of instances are adjusted according to 
        the error of the current prediction. As such, subsequent regressors 
        focus more on difficult cases.
    
    fold: integer, default = 10
        Number of folds to be used in Kfold CV. Must be at least 2.
    
    n_estimators: integer, default = 10
        The number of base estimators in the ensemble.
        In case of perfect fit, the learning procedure is stopped early.

    round: integer, default = 4
        Number of decimal places the metrics in the score grid will be rounded to.

    choose_better: Boolean, default = False
        When set to set to True, base estimator is returned when the metric doesn't 
        improve by ensemble_model. This gurantees the returned object would perform 
        atleast equivalent to base estimator created using create_model or model 
        returned by compare_models.

    optimize: string, default = 'R2'
        Only used when choose_better is set to True. optimize parameter is used
        to compare emsembled model with base estimator. Values accepted in 
        optimize parameter are 'MAE', 'MSE', 'RMSE', 'R2', 'RMSLE', 'MAPE'.

    verbose: Boolean, default = True
        Score grid is not printed when verbose is set to False.


    Returns
    -------
    score_grid
        A table containing the scores of the model across the kfolds. 
        Scoring metrics used are MAE, MSE, RMSE, R2, RMSLE and MAPE.
        Mean and standard deviation of the scores across the folds are 
        also returned.

    model
        Trained ensembled model object.
    
    """
    
    
    '''
    
    ERROR HANDLING STARTS HERE
    
    '''
    
    import logging

    try:
        hasattr(logger, 'name')
    except:
        logger = logging.getLogger('logs')
        logger.setLevel(logging.DEBUG)
        
        # create console handler and set level to debug
        if logger.hasHandlers():
            logger.handlers.clear()
        
        ch = logging.FileHandler('logs.log')
        ch.setLevel(logging.DEBUG)

        # create formatter
        formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        logger.addHandler(ch)

    logger.info("Initializing ensemble_model()")
    logger.info("""ensemble_model(estimator={}, method={}, fold={}, n_estimators={}, round={}, choose_better={}, optimize={}, verbose={})""".\
        format(str(estimator), str(method), str(fold), str(n_estimators), str(round), str(choose_better), str(optimize), str(verbose)))

    logger.info("Checking exceptions")

    #exception checking   
    import sys
        
    #run_time
    import datetime, time
    runtime_start = time.time()

    #Check for allowed method
    available_method = ['Bagging', 'Boosting']
    if method not in available_method:
        sys.exit("(Value Error): Method parameter only accepts two values 'Bagging' or 'Boosting'.")
    
    #checking fold parameter
    if type(fold) is not int:
        sys.exit('(Type Error): Fold parameter only accepts integer value.')
    
    #checking n_estimators parameter
    if type(n_estimators) is not int:
        sys.exit('(Type Error): n_estimators parameter only accepts integer value.')
    
    #checking round parameter
    if type(round) is not int:
        sys.exit('(Type Error): Round parameter only accepts integer value.')
 
    #checking verbose parameter
    if type(verbose) is not bool:
        sys.exit('(Type Error): Verbose parameter can only take argument as True or False.') 
    
    '''
    
    ERROR HANDLING ENDS HERE
    
    '''    
    
    logger.info("Preloading libraries")

    #pre-load libraries
    import pandas as pd
    import datetime, time
    import ipywidgets as ipw
    from IPython.display import display, HTML, clear_output, update_display
    
    logger.info("Preparing display monitor")

    #progress bar
    progress = ipw.IntProgress(value=0, min=0, max=fold+4, step=1 , description='Processing: ')
    master_display = pd.DataFrame(columns=['MAE','MSE','RMSE', 'R2', 'RMSLE', 'MAPE'])
    if verbose:
        if html_param:
            display(progress)
    
    #display monitor
    timestampStr = datetime.datetime.now().strftime("%H:%M:%S")
    monitor = pd.DataFrame( [ ['Initiated' , '. . . . . . . . . . . . . . . . . .', timestampStr ], 
                             ['Status' , '. . . . . . . . . . . . . . . . . .' , 'Loading Dependencies' ],
                             ['ETC' , '. . . . . . . . . . . . . . . . . .',  'Calculating ETC'] ],
                              columns=['', ' ', '   ']).set_index('')
    
    if verbose:
        if html_param:
            display(monitor, display_id = 'monitor')
    
    if verbose:
        if html_param:
            display_ = display(master_display, display_id=True)
            display_id = display_.display_id

    logger.info("Importing libraries")
    
    #dependencies
    import numpy as np
    from sklearn import metrics
    from sklearn.model_selection import KFold   
    
    #ignore warnings
    import warnings
    warnings.filterwarnings('ignore')    
    
    logger.info("Copying training dataset")

    #Storing X_train and y_train in data_X and data_y parameter
    data_X = X_train.copy()
    data_y = y_train.copy()
    
    #reset index
    data_X.reset_index(drop=True, inplace=True)
    data_y.reset_index(drop=True, inplace=True)
      
    progress.value += 1
    
    #defining estimator as model
    model = estimator

    if optimize == 'MAE':
        compare_dimension = 'MAE' 
    elif optimize == 'MSE':
        compare_dimension = 'MSE' 
    elif optimize == 'RMSE':
        compare_dimension = 'RMSE' 
    elif optimize == 'R2':
        compare_dimension = 'R2'
    elif optimize == 'RMSLE':
        compare_dimension = 'RMSLE' 
    elif optimize == 'MAPE':
        compare_dimension = 'MAPE'
    
    logger.info("Checking base model")

    def get_model_name(e):
        return str(e).split("(")[0]

    mn = get_model_name(estimator)

    if 'catboost' in str(estimator):
        mn = 'CatBoostRegressor'
    
    model_dict = {'ExtraTreesRegressor' : 'et',
                'GradientBoostingRegressor' : 'gbr', 
                'RandomForestRegressor' : 'rf',
                'LGBMRegressor' : 'lightgbm',
                'XGBRegressor' : 'xgboost',
                'AdaBoostRegressor' : 'ada', 
                'DecisionTreeRegressor' : 'dt', 
                'Ridge' : 'ridge',
                'TheilSenRegressor' : 'tr', 
                'BayesianRidge' : 'br',
                'LinearRegression' : 'lr',
                'ARDRegression' : 'ard', 
                'KernelRidge' : 'kr', 
                'RANSACRegressor' : 'ransac', 
                'HuberRegressor' : 'huber', 
                'Lasso' : 'lasso', 
                'ElasticNet' : 'en', 
                'Lars' : 'lar', 
                'OrthogonalMatchingPursuit' : 'omp', 
                'MLPRegressor' : 'mlp',
                'KNeighborsRegressor' : 'knn',
                'SVR' : 'svm',
                'LassoLars' : 'llar',
                'PassiveAggressiveRegressor' : 'par',
                'CatBoostRegressor' : 'catboost'}

    estimator__ = model_dict.get(mn)

    model_dict_logging = {'ExtraTreesRegressor' : 'Extra Trees Regressor',
                        'GradientBoostingRegressor' : 'Gradient Boosting Regressor', 
                        'RandomForestRegressor' : 'Random Forest',
                        'LGBMRegressor' : 'Light Gradient Boosting Machine',
                        'XGBRegressor' : 'Extreme Gradient Boosting',
                        'AdaBoostRegressor' : 'AdaBoost Regressor', 
                        'DecisionTreeRegressor' : 'Decision Tree', 
                        'Ridge' : 'Ridge Regression',
                        'TheilSenRegressor' : 'TheilSen Regressor', 
                        'BayesianRidge' : 'Bayesian Ridge',
                        'LinearRegression' : 'Linear Regression',
                        'ARDRegression' : 'Automatic Relevance Determination', 
                        'KernelRidge' : 'Kernel Ridge', 
                        'RANSACRegressor' : 'Random Sample Consensus', 
                        'HuberRegressor' : 'Huber Regressor', 
                        'Lasso' : 'Lasso Regression', 
                        'ElasticNet' : 'Elastic Net', 
                        'Lars' : 'Least Angle Regression', 
                        'OrthogonalMatchingPursuit' : 'Orthogonal Matching Pursuit', 
                        'MLPRegressor' : 'Multi Level Perceptron',
                        'KNeighborsRegressor' : 'K Neighbors Regressor',
                        'SVR' : 'Support Vector Machine',
                        'LassoLars' : 'Lasso Least Angle Regression',
                        'PassiveAggressiveRegressor' : 'Passive Aggressive Regressor',
                        'CatBoostRegressor' : 'CatBoost Regressor',
                        'BaggingRegressor' : 'Bagging Regressor'}

    logger.info('Base model : ' + str(model_dict_logging.get(mn)))

    '''
    MONITOR UPDATE STARTS
    '''
    
    monitor.iloc[1,1:] = 'Selecting Estimator'
    if verbose:
        if html_param:
            update_display(monitor, display_id = 'monitor')
    
    '''
    MONITOR UPDATE ENDS
    '''
    
    if method == 'Bagging':
        
        from sklearn.ensemble import BaggingRegressor
        model = BaggingRegressor(model,bootstrap=True,n_estimators=n_estimators, random_state=seed)
        logger.info("BaggingRegressor() succesfully imported") 
    else:
        
        from sklearn.ensemble import AdaBoostRegressor
        model = AdaBoostRegressor(model, n_estimators=n_estimators, random_state=seed)
        logger.info("AdaBoostRegressor() succesfully imported")

    progress.value += 1
    
    '''
    MONITOR UPDATE STARTS
    '''
    
    monitor.iloc[1,1:] = 'Initializing CV'
    if verbose:
        if html_param:
            update_display(monitor, display_id = 'monitor')
    
    '''
    MONITOR UPDATE ENDS
    '''
    logger.info("Defining folds")
    kf = KFold(fold, random_state=seed, shuffle=folds_shuffle_param)
    
    score_mae =np.empty((0,0))
    score_mse =np.empty((0,0))
    score_rmse =np.empty((0,0))
    score_rmsle =np.empty((0,0))
    score_r2 =np.empty((0,0))
    score_mape =np.empty((0,0))
    score_training_time=np.empty((0,0))
    avgs_mae =np.empty((0,0))
    avgs_mse =np.empty((0,0))
    avgs_rmse =np.empty((0,0))
    avgs_rmsle =np.empty((0,0))
    avgs_r2 =np.empty((0,0))
    avgs_mape =np.empty((0,0))
    avgs_training_time=np.empty((0,0))
    
    def calculate_mape(actual, prediction):
        mask = actual != 0
        return (np.fabs(actual - prediction)/actual)[mask].mean()
    
    fold_num = 1 
    
    for train_i , test_i in kf.split(data_X,data_y):
        
        logger.info("Initializing Fold " + str(fold_num))
        
        t0 = time.time()
        
        '''
        MONITOR UPDATE STARTS
        '''
    
        monitor.iloc[1,1:] = 'Fitting Fold ' + str(fold_num) + ' of ' + str(fold)
        if verbose:
            if html_param:
                update_display(monitor, display_id = 'monitor')

        '''
        MONITOR UPDATE ENDS
        '''
        
        Xtrain,Xtest = data_X.iloc[train_i], data_X.iloc[test_i]
        ytrain,ytest = data_y.iloc[train_i], data_y.iloc[test_i]
        time_start=time.time()
        logger.info("Fitting Model")
        model.fit(Xtrain,ytrain)
        logger.info("Evaluating Metrics")
        pred_ = model.predict(Xtest)
        
        try:
            pred_ = target_inverse_transformer.inverse_transform(np.array(pred_).reshape(-1,1))
            ytest = target_inverse_transformer.inverse_transform(np.array(ytest).reshape(-1,1))
            pred_ = np.nan_to_num(pred_)
            ytest = np.nan_to_num(ytest)
            
        except:
            pass

        logger.info("Compiling Metrics") 
        time_end=time.time()
        mae = metrics.mean_absolute_error(ytest,pred_)
        mse = metrics.mean_squared_error(ytest,pred_)
        rmse = np.sqrt(mse)
        rmsle = np.sqrt(np.mean(np.power(np.log(np.array(abs(pred_))+1) - np.log(np.array(abs(ytest))+1), 2)))
        r2 = metrics.r2_score(ytest,pred_)
        mape = calculate_mape(ytest,pred_)
        training_time=time_end-time_start
        score_mae = np.append(score_mae,mae)
        score_mse = np.append(score_mse,mse)
        score_rmse = np.append(score_rmse,rmse)
        score_rmsle = np.append(score_rmsle,rmsle)
        score_r2 =np.append(score_r2,r2)
        score_mape = np.append(score_mape,mape)
        score_training_time=np.append(score_training_time,training_time)
        
        progress.value += 1
        
                
        '''
        
        This section is created to update_display() as code loops through the fold defined.
        
        '''
        
        fold_results = pd.DataFrame({'MAE':[mae], 'MSE': [mse], 'RMSE': [rmse], 
                                     'R2': [r2], 'RMSLE': [rmsle], 'MAPE': [mape]}).round(round)
        master_display = pd.concat([master_display, fold_results],ignore_index=True)
        fold_results = []
        
        '''
        
        TIME CALCULATION SUB-SECTION STARTS HERE
        
        '''
        t1 = time.time()
        
        tt = (t1 - t0) * (fold-fold_num) / 60
        tt = np.around(tt, 2)
        
        if tt < 1:
            tt = str(np.around((tt * 60), 2))
            ETC = tt + ' Seconds Remaining'
                
        else:
            tt = str (tt)
            ETC = tt + ' Minutes Remaining'
            
        if verbose:
            if html_param:
                update_display(ETC, display_id = 'ETC')
            
        fold_num += 1
        
        
        '''
        MONITOR UPDATE STARTS
        '''

        monitor.iloc[2,1:] = ETC
        
        if verbose:
            if html_param:
                update_display(monitor, display_id = 'monitor')

        '''
        MONITOR UPDATE ENDS
        '''
        
        '''
        
        TIME CALCULATION ENDS HERE
        
        '''

        if verbose:
            if html_param:
                update_display(master_display, display_id = display_id)
        
        '''
        
        Update_display() ends here
        
        '''

    logger.info("Calculating mean and std")    
    mean_mae=np.mean(score_mae)
    mean_mse=np.mean(score_mse)
    mean_rmse=np.mean(score_rmse)
    mean_rmsle=np.mean(score_rmsle)
    mean_r2=np.mean(score_r2)
    mean_mape=np.mean(score_mape)
    mean_training_time=np.mean(score_training_time)
    std_mae=np.std(score_mae)
    std_mse=np.std(score_mse)
    std_rmse=np.std(score_rmse)
    std_rmsle=np.std(score_rmsle)
    std_r2=np.std(score_r2)
    std_mape=np.std(score_mape)
    std_training_time=np.std(score_training_time)
    
    avgs_mae = np.append(avgs_mae, mean_mae)
    avgs_mae = np.append(avgs_mae, std_mae) 
    avgs_mse = np.append(avgs_mse, mean_mse)
    avgs_mse = np.append(avgs_mse, std_mse)
    avgs_rmse = np.append(avgs_rmse, mean_rmse)
    avgs_rmse = np.append(avgs_rmse, std_rmse)
    avgs_rmsle = np.append(avgs_rmsle, mean_rmsle)
    avgs_rmsle = np.append(avgs_rmsle, std_rmsle)
    avgs_r2 = np.append(avgs_r2, mean_r2)
    avgs_r2 = np.append(avgs_r2, std_r2)
    avgs_mape = np.append(avgs_mape, mean_mape)
    avgs_mape = np.append(avgs_mape, std_mape)
    avgs_training_time=np.append(avgs_training_time, mean_training_time)
    avgs_training_time=np.append(avgs_training_time, std_training_time)

    logger.info("Creating metrics dataframe")
    model_results = pd.DataFrame({'MAE': score_mae, 'MSE': score_mse, 'RMSE' : score_rmse, 'R2' : score_r2,
                                  'RMSLE' : score_rmsle, 'MAPE' : score_mape})
    model_avgs = pd.DataFrame({'MAE': avgs_mae, 'MSE': avgs_mse, 'RMSE' : avgs_rmse, 'R2' : avgs_r2,
                                'RMSLE' : avgs_rmsle, 'MAPE' : avgs_mape},index=['Mean', 'SD'])

    model_results = model_results.append(model_avgs)
    model_results = model_results.round(round)  
    
    # yellow the mean
    model_results=model_results.style.apply(lambda x: ['background: yellow ' if (x.name == 'Mean') else '' for i in x], axis=1)
    model_results = model_results.set_precision(round)
    
    progress.value += 1
    
    #refitting the model on complete X_train, y_train
    monitor.iloc[1,1:] = 'Finalizing Model'
    monitor.iloc[2,1:] = 'Almost Finished'
    if verbose:
        if html_param:
            update_display(monitor, display_id = 'monitor')
    
    
    model_fit_start = time.time()
    logger.info("Finalizing model")
    model.fit(data_X, data_y)
    model_fit_end = time.time()

    model_fit_time = np.array(model_fit_end - model_fit_start).round(2)

    #storing results in create_model_container
    logger.info("Uploading results into container")
    create_model_container.append(model_results.data)
    display_container.append(model_results.data)

    #storing results in master_model_container
    logger.info("Uploading model into container")
    master_model_container.append(model)
    
    progress.value += 1
    
    '''
    When choose_better sets to True. optimize metric in scoregrid is
    compared with base model created using create_model so that ensemble_model
    functions return the model with better score only. This will ensure 
    model performance is atleast equivalent to what is seen is compare_models 
    '''
    if choose_better:
        
        logger.info("choose_better activated")

        if verbose:
            if html_param:
                monitor.iloc[1,1:] = 'Compiling Final Results'
                monitor.iloc[2,1:] = 'Almost Finished'
                update_display(monitor, display_id = 'monitor')

        #creating base model for comparison
        logger.info("SubProcess create_model() called ==================================")
        base_model = create_model(estimator=estimator, verbose = False)
        logger.info("SubProcess create_model() end ==================================")
        base_model_results = create_model_container[-1][compare_dimension][-2:][0]
        ensembled_model_results = create_model_container[-2][compare_dimension][-2:][0]

        if compare_dimension == 'R2':
            if ensembled_model_results > base_model_results:
                model = model
            else:
                model = base_model
        else:
            if ensembled_model_results < base_model_results:
                model = model
            else:
                model = base_model

        #re-instate display_constainer state 
        display_container.pop(-1)
        logger.info("choose_better completed")
    
    #end runtime
    runtime_end = time.time()
    runtime = np.array(runtime_end - runtime_start).round(2)
    
    if logging_param:

        logger.info("Creating MLFlow logs")

        #Creating Logs message monitor
        monitor.iloc[1,1:] = 'Creating Logs'
        monitor.iloc[2,1:] = 'Almost Finished'    
        if verbose:
            if html_param:
                update_display(monitor, display_id = 'monitor')


        import mlflow
        from pathlib import Path
        import os

        mlflow.set_experiment(exp_name_log)
        full_name = model_dict_logging.get(mn)

        with mlflow.start_run(run_name=full_name) as run:        

            # Get active run to log as tag
            RunID = mlflow.active_run().info.run_id

            params = model.get_params()

            for i in list(params):
                v = params.get(i)
                if len(str(v)) > 250:
                    params.pop(i)

            mlflow.log_params(params)
            mlflow.log_metrics({"MAE": avgs_mae[0], "MSE": avgs_mse[0], "RMSE": avgs_rmse[0], "R2" : avgs_r2[0],
                                "RMSLE": avgs_rmsle[0], "MAPE": avgs_mape[0]})

            #set tag of compare_models
            mlflow.set_tag("Source", "ensemble_model")
            
            import secrets
            URI = secrets.token_hex(nbytes=4)
            mlflow.set_tag("URI", URI)
            mlflow.set_tag("USI", USI) 
            mlflow.set_tag("Run Time", runtime)
            mlflow.set_tag("Run ID", RunID)

            # Log training time in seconds
            mlflow.log_metric("TT", model_fit_time)

            # Generate hold-out predictions and save as html
            holdout = predict_model(model, verbose=False)
            holdout_score = pull()
            del(holdout)
            display_container.pop(-1)
            holdout_score.to_html('Holdout.html', col_space=65, justify='left')
            mlflow.log_artifact('Holdout.html')
            os.remove('Holdout.html')

            # Log AUC and Confusion Matrix plot
            if log_plots_param:

                logger.info("SubProcess plot_model() called ==================================")

                try:
                    plot_model(model, plot = 'residuals', verbose=False, save=True, system=False)
                    mlflow.log_artifact('Residuals.png')
                    os.remove("Residuals.png")
                except:
                    pass

                try:
                    plot_model(model, plot = 'error', verbose=False, save=True, system=False)
                    mlflow.log_artifact('Prediction Error.png')
                    os.remove("Prediction Error.png")
                except:
                    pass

                try:
                    plot_model(model, plot = 'feature', verbose=False, save=True, system=False)
                    mlflow.log_artifact('Feature Importance.png')
                    os.remove("Feature Importance.png")
                except:
                    pass

                logger.info("SubProcess plot_model() end ==================================")

            # Log the CV results as model_results.html artifact
            model_results.data.to_html('Results.html', col_space=65, justify='left')
            mlflow.log_artifact('Results.html')
            os.remove('Results.html')

            # Log model and transformation pipeline
            from copy import deepcopy

            # get default conda env
            from mlflow.sklearn import get_default_conda_env
            default_conda_env = get_default_conda_env()
            default_conda_env['name'] = str(exp_name_log) + '-env'
            default_conda_env.get('dependencies').pop(-3)
            dependencies = default_conda_env.get('dependencies')[-1]
            from pycaret.utils import __version__
            dep = 'pycaret==' + str(__version__())
            dependencies['pip'] = [dep]
            
            # define model signature
            from mlflow.models.signature import infer_signature
            signature = infer_signature(data_before_preprocess.drop([target_param], axis=1))
            input_example = data_before_preprocess.drop([target_param], axis=1).iloc[0].to_dict()

            # log model as sklearn flavor
            prep_pipe_temp = deepcopy(prep_pipe)
            prep_pipe_temp.steps.append(['trained model', model])
            mlflow.sklearn.log_model(prep_pipe_temp, "model", conda_env = default_conda_env, signature = signature, input_example = input_example)
            del(prep_pipe_temp)
            
    if verbose:
        clear_output()
        if html_param:
            display(model_results)
        else:
            print(model_results.data)
    else:
        clear_output()
    
    logger.info("create_model_container: " + str(len(create_model_container)))
    logger.info("master_model_container: " + str(len(master_model_container)))
    logger.info("display_container: " + str(len(display_container)))

    logger.info(str(model))
    logger.info("ensemble_model() succesfully completed......................................")

    return model

def blend_models(estimator_list = 'All', 
                 fold = 10, 
                 round = 4, 
                 choose_better = False, #added in pycaret==2.0.0 
                 optimize = 'R2', #added in pycaret==2.0.0 
                 turbo = True,
                 verbose = True):
    
    """
    This function creates an ensemble meta-estimator that fits a base regressor on 
    the whole dataset. It then averages the predictions to form a final prediction. 
    By default, this function will use all estimators in the model library (excl. 
    the few estimators when turbo is True) or a specific trained estimator passed 
    as a list in estimator_list param. It scores it using Kfold Cross Validation. 
    The output prints the score grid that shows MAE, MSE, RMSE, R2, RMSLE and MAPE 
    by fold (default = 10 Fold). 

    This function returns a trained model object.  

    Example
    --------
    >>> from pycaret.datasets import get_data
    >>> boston = get_data('boston')
    >>> experiment_name = setup(data = boston,  target = 'medv')
    >>> blend_all = blend_models() 

    This will result in VotingRegressor for all models in the library except 'ard',
    'kr' and 'mlp'.
    
    For specific models, you can use:

    >>> lr = create_model('lr')
    >>> rf = create_model('rf')
    >>> knn = create_model('knn')
    >>> blend_three = blend_models(estimator_list = [lr,rf,knn])

    This will create a VotingRegressor of lr, rf and knn.

    Parameters
    ----------
    estimator_list : string ('All') or list of objects, default = 'All'

    fold: integer, default = 10
       Number of folds to be used in Kfold CV. Must be at least 2. 

    round: integer, default = 4
      Number of decimal places the metrics in the score grid will be rounded to.

    choose_better: Boolean, default = False
        When set to True, base estimator is returned when the metric doesn't 
        improve by ensemble_model. This gurantees the returned object would perform 
        atleast equivalent to base estimator created using create_model or model 
        returned by compare_models.

    optimize: string, default = 'R2'
        Only used when choose_better is set to True. optimize parameter is used
        to compare emsembled model with base estimator. Values accepted in 
        optimize parameter are 'MAE', 'MSE', 'RMSE', 'R2', 'RMSLE', 'MAPE'.

    turbo: Boolean, default = True
        When turbo is set to True, it blacklists estimator that uses Radial Kernel.

    verbose: Boolean, default = True
        Score grid is not printed when verbose is set to False.

    Returns
    -------
    score_grid
        A table containing the scores of the model across the kfolds. 
        Scoring metrics used are MAE, MSE, RMSE, R2, RMSLE and MAPE. 
        Mean and standard deviation of the scores across the folds are 
        also returned.

    model
        Trained Voting Regressor model object. 
       
  
    """
    
    
    '''
    
    ERROR HANDLING STARTS HERE
    
    '''
    
    import logging

    try:
        hasattr(logger, 'name')
    except:
        logger = logging.getLogger('logs')
        logger.setLevel(logging.DEBUG)
        
        # create console handler and set level to debug
        if logger.hasHandlers():
            logger.handlers.clear()
        
        ch = logging.FileHandler('logs.log')
        ch.setLevel(logging.DEBUG)

        # create formatter
        formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        logger.addHandler(ch)

    logger.info("Initializing blend_models()")
    logger.info("""blend_models(estimator_list={}, fold={}, round={}, choose_better={}, optimize={}, turbo={}, verbose={})""".\
        format(str(estimator_list), str(fold), str(round), str(choose_better), str(optimize), str(turbo), str(verbose)))

    logger.info("Checking exceptions")
    
    #exception checking   
    import sys
    
    #run_time
    import datetime, time
    runtime_start = time.time()

    if estimator_list != 'All':
        if type(estimator_list) is not list:
            sys.exit("(Value Error): estimator_list parameter only accepts 'All' as string or list of trained models.")

    #checking error for estimator_list (string)
    if estimator_list != 'All':
        for i in estimator_list:
            if 'sklearn' not in str(type(i)) and 'CatBoostRegressor' not in str(type(i)):
                sys.exit("(Value Error): estimator_list parameter only accepts 'All' as string or trained model object.")
   
    #checking fold parameter
    if type(fold) is not int:
        sys.exit('(Type Error): Fold parameter only accepts integer value.')
    
    #checking round parameter
    if type(round) is not int:
        sys.exit('(Type Error): Round parameter only accepts integer value.')
    
    #checking verbose parameter
    if type(verbose) is not bool:
        sys.exit('(Type Error): Verbose parameter can only take argument as True or False.') 
        
    '''
    
    ERROR HANDLING ENDS HERE
    
    '''
    

    logger.info("Preloading libraries")
    #pre-load libraries
    import pandas as pd
    import time, datetime
    import ipywidgets as ipw
    from IPython.display import display, HTML, clear_output, update_display

    logger.info("Preparing display monitor") 
    #progress bar
    progress = ipw.IntProgress(value=0, min=0, max=fold+4, step=1 , description='Processing: ')
    master_display = pd.DataFrame(columns=['MAE','MSE','RMSE', 'R2', 'RMSLE', 'MAPE'])
    if verbose:
        if html_param:
            display(progress)
    
    #display monitor
    timestampStr = datetime.datetime.now().strftime("%H:%M:%S")
    monitor = pd.DataFrame( [ ['Initiated' , '. . . . . . . . . . . . . . . . . .', timestampStr ], 
                             ['Status' , '. . . . . . . . . . . . . . . . . .' , 'Loading Dependencies' ],
                             ['ETC' , '. . . . . . . . . . . . . . . . . .',  'Calculating ETC'] ],
                              columns=['', ' ', '   ']).set_index('')
    
    if verbose:
        if html_param:
            display(monitor, display_id = 'monitor')
    
    if verbose:
        if html_param:
            display_ = display(master_display, display_id=True)
            display_id = display_.display_id
        
    #ignore warnings
    import warnings
    warnings.filterwarnings('ignore') 
    
    logger.info("Importing libraries")
    #general dependencies
    import numpy as np
    from sklearn import metrics
    from sklearn.model_selection import KFold  
    from sklearn.ensemble import VotingRegressor
    import re
    
    logger.info("Copying training dataset")
    #Storing X_train and y_train in data_X and data_y parameter
    data_X = X_train.copy()
    data_y = y_train.copy()
    
    #reset index
    data_X.reset_index(drop=True, inplace=True)
    data_y.reset_index(drop=True, inplace=True)
    
    if optimize == 'MAE':
        compare_dimension = 'MAE' 
    elif optimize == 'MSE':
        compare_dimension = 'MSE' 
    elif optimize == 'RMSE':
        compare_dimension = 'RMSE' 
    elif optimize == 'R2':
        compare_dimension = 'R2'
    elif optimize == 'RMSLE':
        compare_dimension = 'RMSLE' 
    elif optimize == 'MAPE':
        compare_dimension = 'MAPE'


    #estimator_list_flag
    if estimator_list == 'All':
        all_flag = True
    else:
        all_flag = False

    progress.value += 1
    
    logger.info("Declaring metric variables")
    score_mae =np.empty((0,0))
    score_mse =np.empty((0,0))
    score_rmse =np.empty((0,0))
    score_rmsle =np.empty((0,0))
    score_r2 =np.empty((0,0))
    score_mape =np.empty((0,0))
    score_training_time=np.empty((0,0))
    avgs_mae =np.empty((0,0))
    avgs_mse =np.empty((0,0))
    avgs_rmse =np.empty((0,0))
    avgs_rmsle =np.empty((0,0))
    avgs_r2 =np.empty((0,0))
    avgs_mape =np.empty((0,0))
    avgs_training_time=np.empty((0,0))
    
    def calculate_mape(actual, prediction):
        mask = actual != 0
        return (np.fabs(actual - prediction)/actual)[mask].mean()

    logger.info("Defining folds")
    kf = KFold(fold, random_state=seed, shuffle=folds_shuffle_param)
    
    '''
    MONITOR UPDATE STARTS
    '''
    
    monitor.iloc[1,1:] = 'Compiling Estimators'
    if verbose:
        if html_param:
            update_display(monitor, display_id = 'monitor')
    
    '''
    MONITOR UPDATE ENDS
    '''
    
    if estimator_list == 'All':
        logger.info("Importing untrained models")
        from sklearn.linear_model import LinearRegression
        from sklearn.linear_model import Ridge
        from sklearn.linear_model import Lasso
        from sklearn.linear_model import ElasticNet
        from sklearn.linear_model import Lars
        from sklearn.linear_model import LassoLars
        from sklearn.linear_model import OrthogonalMatchingPursuit
        from sklearn.linear_model import BayesianRidge
        from sklearn.linear_model import ARDRegression
        from sklearn.linear_model import PassiveAggressiveRegressor
        from sklearn.linear_model import RANSACRegressor
        from sklearn.linear_model import TheilSenRegressor
        from sklearn.linear_model import HuberRegressor
        from sklearn.kernel_ridge import KernelRidge
        from sklearn.svm import SVR
        from sklearn.neighbors import KNeighborsRegressor
        from sklearn.tree import DecisionTreeRegressor
        from sklearn.ensemble import RandomForestRegressor
        from sklearn.ensemble import ExtraTreesRegressor
        from sklearn.ensemble import AdaBoostRegressor
        from sklearn.ensemble import GradientBoostingRegressor
        from sklearn.neural_network import MLPRegressor
        from xgboost import XGBRegressor
        import lightgbm as lgb
        from catboost import CatBoostRegressor

        lr = LinearRegression(n_jobs=n_jobs_param)
        lasso = Lasso(random_state=seed)
        ridge = Ridge(random_state=seed)
        en = ElasticNet(random_state=seed)
        lar = Lars()
        llar = LassoLars()
        omp = OrthogonalMatchingPursuit()
        br = BayesianRidge()
        ard = ARDRegression()
        par = PassiveAggressiveRegressor(random_state=seed)
        ransac = RANSACRegressor(min_samples=0.5, random_state=seed)
        tr = TheilSenRegressor(random_state=seed, n_jobs=n_jobs_param)
        huber = HuberRegressor()
        kr = KernelRidge()
        svm = SVR()
        knn = KNeighborsRegressor(n_jobs=n_jobs_param)
        dt = DecisionTreeRegressor(random_state=seed)
        rf = RandomForestRegressor(random_state=seed, n_jobs=n_jobs_param)
        et = ExtraTreesRegressor(random_state=seed, n_jobs=n_jobs_param)
        ada = AdaBoostRegressor(random_state=seed)
        gbr = GradientBoostingRegressor(random_state=seed)
        mlp = MLPRegressor(random_state=seed)
        xgboost = XGBRegressor(random_state=seed, n_jobs=n_jobs_param, verbosity=0)
        lightgbm = lgb.LGBMRegressor(random_state=seed, n_jobs=n_jobs_param)
        catboost = CatBoostRegressor(random_state=seed, silent = True, thread_count=n_jobs_param)

        logger.info("Import successful")

        progress.value += 1
        
        if turbo:
            
            estimator_list = [lr, lasso, ridge, en, lar, llar, omp, br, par, ransac, tr, huber, 
                             svm, knn, dt, rf, et, ada, gbr, xgboost, lightgbm, catboost]

        else:
            
            estimator_list = [lr, lasso, ridge, en, lar, llar, omp, br, ard, par, ransac, tr, huber, kr, 
                             svm, knn, dt, rf, et, ada, gbr, mlp, xgboost, lightgbm, catboost]
            

    else:

        estimator_list = estimator_list
        
    logger.info("Defining model names in estimator_list")
    model_names = []

    for names in estimator_list:

        model_names = np.append(model_names, str(names).split("(")[0])
        
    model_names_fixed = []
    
    for i in model_names:
        if 'CatBoostRegressor' in i:
            model_names_fixed.append('CatBoost Regressor')
        else:
            model_names_fixed.append(i)
        
    model_names = model_names_fixed

    def putSpace(input):
        words = re.findall('[A-Z][a-z]*', input)
        words = ' '.join(words)
        return words  

    model_names_modified = []
    
    for i in model_names:
        
        model_names_modified.append(putSpace(i))
        model_names = model_names_modified
    
    model_names_final = []
  
    for j in model_names_modified:

        if j == 'A R D Regression':
            model_names_final.append('Automatic Relevance Determination')

        elif j == 'M L P Regressor':
            model_names_final.append('MLP Regressor')

        elif j == 'R A N S A C Regressor':
            model_names_final.append('RANSAC Regressor')

        elif j == 'S V R':
            model_names_final.append('Support Vector Regressor')
            
        elif j == 'Lars':
            model_names_final.append('Least Angle Regression')
            
        elif j == 'X G B Regressor':
            model_names_final.append('Extreme Gradient Boosting Regressor')

        elif j == 'L G B M Regressor':
            model_names_final.append('Light Gradient Boosting Machine')
            
        elif j == 'Cat Boost Regressor':
            model_names_final.append('CatBoost Regressor')        
            
        else: 
            model_names_final.append(j)
            
    model_names = model_names_final

    model_names_n = []
    counter = 0
    
    for i in model_names:
        mn = str(i) + '_' + str(counter)
        model_names_n.append(mn)
        counter += 1
        
    model_names = model_names_n

    estimator_list = estimator_list
    
    estimator_list_ = zip(model_names, estimator_list)
    estimator_list_ = list(estimator_list_)

    try:
        model = VotingRegressor(estimators=estimator_list_, n_jobs=n_jobs_param)
        model.fit(data_X,data_y)
        logger.info("n_jobs multiple passed")
    except:
        logger.info("n_jobs multiple failed")
        model = VotingRegressor(estimators=estimator_list_)
    
    progress.value += 1
    
    '''
    MONITOR UPDATE STARTS
    '''
    
    monitor.iloc[1,1:] = 'Initializing CV'
    if verbose:
        if html_param:
            update_display(monitor, display_id = 'monitor')
    
    '''
    MONITOR UPDATE ENDS
    '''
    
    fold_num = 1
    
    for train_i , test_i in kf.split(data_X,data_y):
        
        logger.info("Initializing Fold " + str(fold_num))
        
        progress.value += 1
        
        t0 = time.time()
        
        '''
        MONITOR UPDATE STARTS
        '''
    
        monitor.iloc[1,1:] = 'Fitting Fold ' + str(fold_num) + ' of ' + str(fold)

        if verbose:
            if html_param:
                update_display(monitor, display_id = 'monitor')

        '''
        MONITOR UPDATE ENDS
        '''
    
        Xtrain,Xtest = data_X.iloc[train_i], data_X.iloc[test_i]
        ytrain,ytest = data_y.iloc[train_i], data_y.iloc[test_i]      
        time_start=time.time()
        logger.info("Fitting Model")
        model.fit(Xtrain,ytrain)
        logger.info("Evaluating Metrics")
        pred_ = model.predict(Xtest)
        
        try:
            pred_ = target_inverse_transformer.inverse_transform(np.array(pred_).reshape(-1,1))
            ytest = target_inverse_transformer.inverse_transform(np.array(ytest).reshape(-1,1))
            pred_ = np.nan_to_num(pred_)
            ytest = np.nan_to_num(ytest)
            
        except:
            pass
        
        logger.info("Compiling Metrics")
        time_end=time.time()
        mae = metrics.mean_absolute_error(ytest,pred_)
        mse = metrics.mean_squared_error(ytest,pred_)
        rmse = np.sqrt(mse)
        rmsle = np.sqrt(np.mean(np.power(np.log(np.array(abs(pred_))+1) - np.log(np.array(abs(ytest))+1), 2)))
        r2 = metrics.r2_score(ytest,pred_)
        mape = calculate_mape(ytest,pred_)
        training_time=time_end-time_start
        score_mae = np.append(score_mae,mae)
        score_mse = np.append(score_mse,mse)
        score_rmse = np.append(score_rmse,rmse)
        score_rmsle = np.append(score_rmsle,rmsle)
        score_r2 =np.append(score_r2,r2)
        score_mape = np.append(score_mape,mape)
        score_training_time=np.append(score_training_time,training_time)
    
        '''
        
        This section handles time calculation and is created to update_display() as code loops through 
        the fold defined.
        
        '''
        
        fold_results = pd.DataFrame({'MAE':[mae], 'MSE': [mse], 'RMSE': [rmse], 
                                     'R2': [r2], 'RMSLE': [rmsle], 'MAPE': [mape]}).round(round)
        master_display = pd.concat([master_display, fold_results],ignore_index=True)
        fold_results = []
        
        '''
        TIME CALCULATION SUB-SECTION STARTS HERE
        '''
        t1 = time.time()
        
        tt = (t1 - t0) * (fold-fold_num) / 60
        tt = np.around(tt, 2)
        
        if tt < 1:
            tt = str(np.around((tt * 60), 2))
            ETC = tt + ' Seconds Remaining'
                
        else:
            tt = str (tt)
            ETC = tt + ' Minutes Remaining'
            
        fold_num += 1
        
        '''
        MONITOR UPDATE STARTS
        '''

        monitor.iloc[2,1:] = ETC
        if verbose:
            if html_param:
                update_display(monitor, display_id = 'monitor')

        '''
        MONITOR UPDATE ENDS
        '''
        
        '''
        TIME CALCULATION ENDS HERE
        '''
        
        if verbose:
            if html_param:
                update_display(master_display, display_id = display_id)
            
        
        '''
        
        Update_display() ends here
        
        '''
    logger.info("Calculating mean and std")
    mean_mae=np.mean(score_mae)
    mean_mse=np.mean(score_mse)
    mean_rmse=np.mean(score_rmse)
    mean_rmsle=np.mean(score_rmsle)
    mean_r2=np.mean(score_r2)
    mean_mape=np.mean(score_mape)
    mean_training_time=np.mean(score_training_time)
    std_mae=np.std(score_mae)
    std_mse=np.std(score_mse)
    std_rmse=np.std(score_rmse)
    std_rmsle=np.std(score_rmsle)
    std_r2=np.std(score_r2)
    std_mape=np.std(score_mape)
    std_training_time=np.std(score_training_time)
    
    avgs_mae = np.append(avgs_mae, mean_mae)
    avgs_mae = np.append(avgs_mae, std_mae) 
    avgs_mse = np.append(avgs_mse, mean_mse)
    avgs_mse = np.append(avgs_mse, std_mse)
    avgs_rmse = np.append(avgs_rmse, mean_rmse)
    avgs_rmse = np.append(avgs_rmse, std_rmse)
    avgs_rmsle = np.append(avgs_rmsle, mean_rmsle)
    avgs_rmsle = np.append(avgs_rmsle, std_rmsle)
    avgs_r2 = np.append(avgs_r2, mean_r2)
    avgs_r2 = np.append(avgs_r2, std_r2)
    avgs_mape = np.append(avgs_mape, mean_mape)
    avgs_mape = np.append(avgs_mape, std_mape)
    avgs_training_time=np.append(avgs_training_time, mean_training_time)
    avgs_training_time=np.append(avgs_training_time, std_training_time)
    
    
    progress.value += 1
    
    logger.info("Creating metrics dataframe")
    model_results = pd.DataFrame({'MAE': score_mae, 'MSE': score_mse, 'RMSE' : score_rmse, 'R2' : score_r2,
                                  'RMSLE' : score_rmsle, 'MAPE' : score_mape})
    model_avgs = pd.DataFrame({'MAE': avgs_mae, 'MSE': avgs_mse, 'RMSE' : avgs_rmse, 'R2' : avgs_r2,
                                'RMSLE' : avgs_rmsle, 'MAPE' : avgs_mape},index=['Mean', 'SD'])

    model_results = model_results.append(model_avgs)
    model_results = model_results.round(round)
    
    # yellow the mean
    model_results=model_results.style.apply(lambda x: ['background: yellow' if (x.name == 'Mean') else '' for i in x], axis=1)
    model_results = model_results.set_precision(round)
    progress.value += 1
    
    #refitting the model on complete X_train, y_train
    monitor.iloc[1,1:] = 'Finalizing Model'
    monitor.iloc[2,1:] = 'Almost Finished'
    if verbose:
        if html_param:
            update_display(monitor, display_id = 'monitor')
    
    model_fit_start = time.time()
    logger.info("Finalizing model")
    model.fit(data_X, data_y)
    model_fit_end = time.time()

    model_fit_time = np.array(model_fit_end - model_fit_start).round(2)
    
    progress.value += 1

    #storing results in create_model_container
    logger.info("Uploading results into container")
    create_model_container.append(model_results.data)
    display_container.append(model_results.data)

    #storing results in master_model_container
    logger.info("Uploading model into container")
    master_model_container.append(model)

    '''
    When choose_better sets to True. optimize metric in scoregrid is
    compared with base model created using create_model so that stack_models
    functions return the model with better score only. This will ensure 
    model performance is atleast equivalent to what is seen in compare_models 
    '''
    
    scorer = []

    blend_model_results = create_model_container[-1][compare_dimension][-2:][0]
    
    scorer.append(blend_model_results)

    if choose_better and all_flag is False:
        logger.info("choose_better activated")
        if verbose:
            if html_param:
                monitor.iloc[1,1:] = 'Compiling Final Results'
                monitor.iloc[2,1:] = 'Almost Finished'
                update_display(monitor, display_id = 'monitor')

        base_models_ = []
        logger.info("SubProcess create_model() called ==================================")
        for i in estimator_list:
            m = create_model(i,verbose=False, system=False)
            s = create_model_container[-1][compare_dimension][-2:][0]
            scorer.append(s)
            base_models_.append(m)

            #re-instate display_constainer state 
            display_container.pop(-1)

        logger.info("SubProcess create_model() called ==================================")
        logger.info("choose_better completed")

    if compare_dimension == 'R2':
        index_scorer = scorer.index(max(scorer))
    else:
        index_scorer = scorer.index(min(scorer))

    if index_scorer == 0:
        model = model
    else:
        model = base_models_[index_scorer-1]

   #end runtime
    runtime_end = time.time()
    runtime = np.array(runtime_end - runtime_start).round(2)

    if logging_param:
        
        logger.info("Creating MLFlow logs")

        #Creating Logs message monitor
        monitor.iloc[1,1:] = 'Creating Logs'
        monitor.iloc[2,1:] = 'Almost Finished'    
        if verbose:
            if html_param:
                update_display(monitor, display_id = 'monitor')

        import mlflow
        from pathlib import Path
        import os

        with mlflow.start_run(run_name='Voting Regressor') as run:

            # Get active run to log as tag
            RunID = mlflow.active_run().info.run_id

            mlflow.log_metrics({"MAE": avgs_mae[0], "MSE": avgs_mse[0], "RMSE": avgs_rmse[0], "R2" : avgs_r2[0],
                                "RMSLE": avgs_rmsle[0], "MAPE": avgs_mape[0]})

            # Generate hold-out predictions and save as html
            holdout = predict_model(model, verbose=False)
            holdout_score = pull()
            del(holdout)
            display_container.pop(-1)
            holdout_score.to_html('Holdout.html', col_space=65, justify='left')
            mlflow.log_artifact('Holdout.html')
            os.remove('Holdout.html')

            #set tag of compare_models
            mlflow.set_tag("Source", "blend_models")
            
            import secrets
            URI = secrets.token_hex(nbytes=4)
            mlflow.set_tag("URI", URI)
            mlflow.set_tag("USI", USI)
            mlflow.set_tag("Run Time", runtime)
            mlflow.set_tag("Run ID", RunID)

            # Log training time of compare_models
            mlflow.log_metric("TT", model_fit_time)

            # Log AUC and Confusion Matrix plot
            if log_plots_param:

                logger.info("SubProcess plot_model() called ==================================")

                try:
                    plot_model(model, plot = 'residuals', verbose=False, save=True, system=False)
                    mlflow.log_artifact('Residuals.png')
                    os.remove("Residuals.png")
                except:
                    pass

                try:
                    plot_model(model, plot = 'error', verbose=False, save=True, system=False)
                    mlflow.log_artifact('Prediction Error.png')
                    os.remove("Prediction Error.png")
                except:
                    pass

                try:
                    plot_model(model, plot = 'feature', verbose=False, save=True, system=False)
                    mlflow.log_artifact('Feature Importance.png')
                    os.remove("Feature Importance.png")
                except:
                    pass
                
                logger.info("SubProcess plot_model() end ==================================")

            # Log the CV results as model_results.html artifact
            model_results.data.to_html('Results.html', col_space=65, justify='left')
            mlflow.log_artifact('Results.html')
            os.remove('Results.html')

            # Log model and transformation pipeline
            from copy import deepcopy

            # get default conda env
            from mlflow.sklearn import get_default_conda_env
            default_conda_env = get_default_conda_env()
            default_conda_env['name'] = str(exp_name_log) + '-env'
            default_conda_env.get('dependencies').pop(-3)
            dependencies = default_conda_env.get('dependencies')[-1]
            from pycaret.utils import __version__
            dep = 'pycaret==' + str(__version__())
            dependencies['pip'] = [dep]
            
            # define model signature
            from mlflow.models.signature import infer_signature
            signature = infer_signature(data_before_preprocess.drop([target_param], axis=1))
            input_example = data_before_preprocess.drop([target_param], axis=1).iloc[0].to_dict()

            # log model as sklearn flavor
            prep_pipe_temp = deepcopy(prep_pipe)
            prep_pipe_temp.steps.append(['trained model', model])
            mlflow.sklearn.log_model(prep_pipe_temp, "model", conda_env = default_conda_env, signature = signature, input_example = input_example)
            del(prep_pipe_temp)

    if verbose:
        clear_output()
        if html_param:
            display(model_results)
        else:
            print(model_results.data)
    
    logger.info("create_model_container: " + str(len(create_model_container)))
    logger.info("master_model_container: " + str(len(master_model_container)))
    logger.info("display_container: " + str(len(display_container)))

    logger.info(str(model))
    logger.info("blend_models() succesfully completed......................................")

    return model

def stack_models(estimator_list, 
                 meta_model = None, 
                 fold = 10,
                 round = 4, 
                 restack = True, 
                 choose_better = False, #added in pycaret==2.0.0
                 optimize = 'R2', #added in pycaret==2.0.0
                 verbose = True):
    
    """
    This function trains a meta model and scores it using Kfold Cross Validation.
    The predictions from the base level models as passed in the estimator_list param 
    are used as input features for the meta model. The restacking parameter controls
    the ability to expose raw features to the meta model when set to True
    (default = False).

    The output prints a score grid that shows MAE, MSE, RMSE, R2, RMSLE and MAPE by 
    fold (default = 10 Folds).
    
    This function returns a trained model object. 

    Example
    --------
    >>> from pycaret.datasets import get_data
    >>> boston = get_data('boston')
    >>> experiment_name = setup(data = boston,  target = 'medv')
    >>> dt = create_model('dt')
    >>> rf = create_model('rf')
    >>> ada = create_model('ada')
    >>> ridge = create_model('ridge')
    >>> knn = create_model('knn')
    >>>  stacked_models = stack_models(estimator_list=[dt,rf,ada,ridge,knn])

    This will create a meta model that will use the predictions of all the 
    models provided in estimator_list param. By default, the meta model is 
    Linear Regression but can be changed with meta_model param.

    Parameters
    ----------
    estimator_list : list of object

    meta_model : object, default = None
        If set to None, Linear Regression is used as a meta model.

    fold: integer, default = 10
        Number of folds to be used in Kfold CV. Must be at least 2. 

    round: integer, default = 4
        Number of decimal places the metrics in the score grid will be rounded to.

    restack: Boolean, default = True
        When restack is set to True, raw data will be exposed to meta model when
        making predictions, otherwise when False, only the predicted label is passed 
        to meta model when making final predictions.

    choose_better: Boolean, default = False
        When set to True, base estimator is returned when the metric doesn't 
        improve by ensemble_model. This gurantees the returned object would perform 
        atleast equivalent to base estimator created using create_model or model 
        returned by compare_models.

    optimize: string, default = 'R2'
        Only used when choose_better is set to True. optimize parameter is used
        to compare emsembled model with base estimator. Values accepted in 
        optimize parameter are 'MAE', 'MSE', 'RMSE', 'R2', 'RMSLE', 'MAPE'.
    
    verbose: Boolean, default = True
        Score grid is not printed when verbose is set to False.

    Returns
    -------
    score_grid
        A table containing the scores of the model across the kfolds. 
        Scoring metrics used are MAE, MSE, RMSE, R2, RMSLE and MAPE.
        Mean and standard deviation of the scores across the folds are 
        also returned.

    model
        Trained model object.
          
    """
    
    '''
    
    ERROR HANDLING STARTS HERE
    
    '''
    
    import logging

    try:
        hasattr(logger, 'name')
    except:
        logger = logging.getLogger('logs')
        logger.setLevel(logging.DEBUG)
        
        # create console handler and set level to debug
        if logger.hasHandlers():
            logger.handlers.clear()
        
        ch = logging.FileHandler('logs.log')
        ch.setLevel(logging.DEBUG)

        # create formatter
        formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        logger.addHandler(ch)

    logger.info("Initializing stack_models()")
    logger.info("""stack_models(estimator_list={}, meta_model={}, fold={}, round={}, restack={}, choose_better={}, optimize={}, verbose={})""".\
        format(str(estimator_list), str(meta_model), str(fold), str(round), str(restack), str(choose_better), str(optimize), str(verbose)))

    logger.info("Checking exceptions")

    #exception checking   
    import sys
    
    #run_time
    import datetime, time
    runtime_start = time.time()

    #checking error for estimator_list
    for i in estimator_list:
        if 'sklearn' not in str(type(i)) and 'CatBoostRegressor' not in str(type(i)):
            sys.exit("(Value Error): estimator_list parameter only trained model object")
            
    #checking meta model
    if meta_model is not None:
        if 'sklearn' not in str(type(meta_model)) and 'CatBoostRegressor' not in str(type(meta_model)):
            sys.exit("(Value Error): estimator_list parameter only trained model object")
    
    #checking fold parameter
    if type(fold) is not int:
        sys.exit('(Type Error): Fold parameter only accepts integer value.')
    
    #checking round parameter
    if type(round) is not int:
        sys.exit('(Type Error): Round parameter only accepts integer value.')

    #checking restack parameter
    if type(restack) is not bool:
        sys.exit('(Type Error): Restack parameter can only take argument as True or False.')    
        
    #checking verbose parameter
    if type(verbose) is not bool:
        sys.exit('(Type Error): Verbose parameter can only take argument as True or False.') 
        
    '''
    
    ERROR HANDLING ENDS HERE
    
    '''

    logger.info("Preloading libraries")
    #pre-load libraries
    import pandas as pd
    import ipywidgets as ipw
    from IPython.display import display, HTML, clear_output, update_display
    import time, datetime
    from copy import deepcopy
    from sklearn.base import clone
    
    #ignore warnings
    import warnings
    warnings.filterwarnings('ignore') 
    
    logger.info("Defining meta model")
    #Defining meta model. Linear Regression hardcoded for now
    if meta_model == None:
        from sklearn.linear_model import LinearRegression
        meta_model = LinearRegression(n_jobs=n_jobs_param)
    else:
        meta_model = clone(meta_model) 
    
    if optimize == 'MAE':
        compare_dimension = 'MAE' 
    elif optimize == 'MSE':
        compare_dimension = 'MSE' 
    elif optimize == 'RMSE':
        compare_dimension = 'RMSE' 
    elif optimize == 'R2':
        compare_dimension = 'R2'
    elif optimize == 'RMSLE':
        compare_dimension = 'RMSLE' 
    elif optimize == 'MAPE':
        compare_dimension = 'MAPE'

    clear_output()
    
    logger.info("Preparing display monitor")
    #progress bar
    max_progress = fold + 4
    progress = ipw.IntProgress(value=0, min=0, max=max_progress, step=1 , description='Processing: ')
    master_display = pd.DataFrame(columns=['MAE','MSE','RMSE', 'R2', 'RMSLE', 'MAPE'])
    if verbose:
        if html_param:
            display(progress)
    
    #display monitor
    timestampStr = datetime.datetime.now().strftime("%H:%M:%S")
    monitor = pd.DataFrame( [ ['Initiated' , '. . . . . . . . . . . . . . . . . .', timestampStr ], 
                             ['Status' , '. . . . . . . . . . . . . . . . . .' , 'Loading Dependencies' ],
                             ['ETC' , '. . . . . . . . . . . . . . . . . .',  'Calculating ETC'] ],
                              columns=['', ' ', '   ']).set_index('')
    
    if verbose:
        if html_param:
            display(monitor, display_id = 'monitor')
    
    if verbose:
        if html_param:
            display_ = display(master_display, display_id=True)
            display_id = display_.display_id
    
    logger.info("Importing libraries")
    #dependencies
    import numpy as np
    from sklearn import metrics
    from sklearn.model_selection import KFold
    from sklearn.model_selection import cross_val_predict
    from sklearn.ensemble import StackingRegressor
    
    progress.value += 1

    logger.info("Copying training dataset")
    #Storing X_train and y_train in data_X and data_y parameter
    data_X = X_train.copy()
    data_y = y_train.copy()
    
    #reset index
    data_X.reset_index(drop=True, inplace=True)
    data_y.reset_index(drop=True, inplace=True)
    
    logger.info("Defining folds")
    #cross validation setup starts here
    kf = KFold(fold, random_state=seed, shuffle=folds_shuffle_param)
    
    logger.info("Declaring metric variables")

    score_mae =np.empty((0,0))
    score_mse =np.empty((0,0))
    score_rmse =np.empty((0,0))
    score_rmsle =np.empty((0,0))
    score_r2 =np.empty((0,0))
    score_mape =np.empty((0,0))
    score_training_time=np.empty((0,0))
    avgs_mae =np.empty((0,0))
    avgs_mse =np.empty((0,0))
    avgs_rmse =np.empty((0,0))
    avgs_r2 =np.empty((0,0))
    avgs_mape =np.empty((0,0)) 
    avgs_rmsle =np.empty((0,0))
    avgs_training_time=np.empty((0,0))
    
    def calculate_mape(actual, prediction):
        mask = actual != 0
        return (np.fabs(actual - prediction)/actual)[mask].mean()

    logger.info("Getting model names")
    #defining model_library model names
    model_names = np.zeros(0)
    for item in estimator_list:
        model_names = np.append(model_names, str(item).split("(")[0])
    
    model_names_fixed = []
    
    for i in model_names:
        if 'CatBoostRegressor' in i:
            a = 'CatBoostRegressor'
            model_names_fixed.append(a)
        else:
            model_names_fixed.append(i)
            
    model_names = model_names_fixed
    
    model_names_fixed = []
    
    counter = 0
    for i in model_names:
        s = str(i) + '_' + str(counter)
        model_names_fixed.append(s)
        counter += 1
    
    logger.info("Compiling estimator_list parameter")

    counter = 0
    
    estimator_list_tuples = []
    
    for i in estimator_list:
        estimator_list_tuples.append(tuple([model_names_fixed[counter], estimator_list[counter]]))
        counter += 1

    logger.info("Creating StackingRegressor()")

    model = StackingRegressor(estimators = estimator_list_tuples, final_estimator = meta_model, cv = fold,\
            n_jobs = n_jobs_param, passthrough = restack)

    fold_num = 1
    
    for train_i , test_i in kf.split(data_X,data_y):
        
        logger.info("Initializing Fold " + str(fold_num))

        t0 = time.time()
        
        '''
        MONITOR UPDATE STARTS
        '''
    
        monitor.iloc[1,1:] = 'Fitting Fold ' + str(fold_num) + ' of ' + str(fold)
        if verbose:
            if html_param:
                update_display(monitor, display_id = 'monitor')

        '''
        MONITOR UPDATE ENDS
        '''
        
        Xtrain,Xtest = data_X.iloc[train_i], data_X.iloc[test_i]
        ytrain,ytest = data_y.iloc[train_i], data_y.iloc[test_i]  
        time_start=time.time()
        logger.info("Fitting Model")
        model.fit(Xtrain,ytrain)
        logger.info("Evaluating Metrics")
        pred_ = model.predict(Xtest)
        
        try:
            pred_ = target_inverse_transformer.inverse_transform(np.array(pred_).reshape(-1,1))
            ytest = target_inverse_transformer.inverse_transform(np.array(ytest).reshape(-1,1))
            pred_ = np.nan_to_num(pred_)
            ytest = np.nan_to_num(ytest)
            
        except:
            pass
            logger.info("No inverse transformation")

        logger.info("Compiling Metrics")
        time_end=time.time()
        mae = metrics.mean_absolute_error(ytest,pred_)
        mse = metrics.mean_squared_error(ytest,pred_)
        rmse = np.sqrt(mse)
        rmsle = np.sqrt(np.mean(np.power(np.log(np.array(abs(pred_))+1) - np.log(np.array(abs(ytest))+1), 2)))
        r2 = metrics.r2_score(ytest,pred_)
        mape = calculate_mape(ytest,pred_)
        training_time=time_end-time_start
        score_mae = np.append(score_mae,mae)
        score_mse = np.append(score_mse,mse)
        score_rmse = np.append(score_rmse,rmse)
        score_rmsle = np.append(score_rmsle,rmsle)
        score_r2 =np.append(score_r2,r2)
        score_mape = np.append(score_mape,mape)
        score_training_time=np.append(score_training_time,training_time)
        progress.value += 1
        
        
        '''
        
        This section handles time calculation and is created to update_display() as code loops through 
        the fold defined.
        
        '''
        
        fold_results = pd.DataFrame({'MAE':[mae], 'MSE': [mse], 'RMSE': [rmse], 'R2': [r2],
                                     'RMSLE' : [rmsle], 'MAPE': [mape] }).round(round)
        master_display = pd.concat([master_display, fold_results],ignore_index=True)
        fold_results = []
        
        '''
        TIME CALCULATION SUB-SECTION STARTS HERE
        '''
        t1 = time.time()
        
        tt = (t1 - t0) * (fold-fold_num) / 60
        tt = np.around(tt, 2)
        
        if tt < 1:
            tt = str(np.around((tt * 60), 2))
            ETC = tt + ' Seconds Remaining'
                
        else:
            tt = str (tt)
            ETC = tt + ' Minutes Remaining'
            
        '''
        MONITOR UPDATE STARTS
        '''

        monitor.iloc[2,1:] = ETC
        if verbose:
            if html_param:
                update_display(monitor, display_id = 'monitor')

        '''
        MONITOR UPDATE ENDS
        '''
            
        fold_num += 1
        
        '''
        TIME CALCULATION ENDS HERE
        '''
        
        if verbose:
            if html_param:
                update_display(master_display, display_id = display_id)
            
        
        '''
        
        Update_display() ends here
        
        '''

    logger.info("Calculating mean and std")

    mean_mae=np.mean(score_mae)
    mean_mse=np.mean(score_mse)
    mean_rmse=np.mean(score_rmse)
    mean_rmsle=np.mean(score_rmsle)
    mean_r2=np.mean(score_r2)
    mean_mape=np.mean(score_mape)
    mean_training_time=np.mean(score_training_time)
    std_mae=np.std(score_mae)
    std_mse=np.std(score_mse)
    std_rmse=np.std(score_rmse)
    std_rmsle=np.std(score_rmsle)
    std_r2=np.std(score_r2)
    std_mape=np.std(score_mape)
    std_training_time=np.std(score_training_time)
    
    avgs_mae = np.append(avgs_mae, mean_mae)
    avgs_mae = np.append(avgs_mae, std_mae) 
    avgs_mse = np.append(avgs_mse, mean_mse)
    avgs_mse = np.append(avgs_mse, std_mse)
    avgs_rmse = np.append(avgs_rmse, mean_rmse)
    avgs_rmse = np.append(avgs_rmse, std_rmse)
    avgs_rmsle = np.append(avgs_rmsle, mean_rmsle)
    avgs_rmsle = np.append(avgs_rmsle, std_rmsle)
    avgs_r2 = np.append(avgs_r2, mean_r2)
    avgs_r2 = np.append(avgs_r2, std_r2)
    avgs_mape = np.append(avgs_mape, mean_mape)
    avgs_mape = np.append(avgs_mape, std_mape)
    avgs_training_time=np.append(avgs_training_time, mean_training_time)
    avgs_training_time=np.append(avgs_training_time, std_training_time)
    
    progress.value += 1
    
    logger.info("Creating metrics dataframe")

    model_results = pd.DataFrame({'MAE': score_mae, 'MSE': score_mse, 'RMSE' : score_rmse, 'R2' : score_r2,
                                  'RMSLE' : score_rmsle, 'MAPE' : score_mape})
    model_avgs = pd.DataFrame({'MAE': avgs_mae, 'MSE': avgs_mse, 'RMSE' : avgs_rmse, 'R2' : avgs_r2,
                                'RMSLE' : avgs_rmsle, 'MAPE' : avgs_mape},index=['Mean', 'SD'])

    model_results = model_results.append(model_avgs)
    model_results = model_results.round(round)
    
    #Yellow the mean
    model_results=model_results.style.apply(lambda x: ['background: yellow' if (x.name == 'Mean') else '' for i in x], axis=1)
    model_results = model_results.set_precision(round)

    #refitting the model on complete X_train, y_train
    monitor.iloc[1,1:] = 'Finalizing Model'
    monitor.iloc[2,1:] = 'Almost Finished'
    if verbose:
        if html_param:
            update_display(monitor, display_id = 'monitor')
    
    model_fit_start = time.time()
    logger.info("Finalizing model")
    model.fit(data_X, data_y)
    model_fit_end = time.time()

    model_fit_time = np.array(model_fit_end - model_fit_start).round(2)
    
    #end runtime
    runtime_end = time.time()
    runtime = np.array(runtime_end - runtime_start).round(2)

    progress.value += 1
    

    '''
    When choose_better sets to True. optimize metric in scoregrid is
    compared with base model created using create_model so that stack_models
    functions return the model with better score only. This will ensure 
    model performance is atleast equivalent to what is seen in compare_models 
    '''
    
    scorer = []

    stack_model_results = create_model_container[-1][compare_dimension][-2:][0]
    
    scorer.append(stack_model_results)
    
    if choose_better:

        logger.info("choose_better activated")

        if verbose:
            if html_param:
                monitor.iloc[1,1:] = 'Compiling Final Results'
                monitor.iloc[2,1:] = 'Almost Finished'
                update_display(monitor, display_id = 'monitor')

        base_models_ = []
        logger.info("SubProcess create_model() called ==================================")
        for i in estimator_list:
            m = create_model(i,verbose=False)
            s = create_model_container[-1][compare_dimension][-2:][0]
            scorer.append(s)
            base_models_.append(m)

        meta_model_clone = clone(meta_model)
        mm = create_model(meta_model_clone, verbose=False)
        base_models_.append(mm)
        s = create_model_container[-1][compare_dimension][-2:][0]
        scorer.append(s)

        #re-instate display_constainer state 
        display_container.pop(-1)
        logger.info("SubProcess create_model() called ==================================")
        logger.info("choose_better completed")

    progress.value += 1

    #returning better model
    if compare_dimension == 'R2':
        index_scorer = scorer.index(max(scorer))
    else:
        index_scorer = scorer.index(min(scorer))

    if index_scorer == 0:
        model = model
    else:
        model = base_models_[index_scorer-1]
    
    #end runtime
    runtime_end = time.time()
    runtime = np.array(runtime_end - runtime_start).round(2)

    progress.value += 1

    if logging_param:
        
        logger.info("Creating MLFlow logs")

        import mlflow
        from pathlib import Path
        import os

        #Creating Logs message monitor
        monitor.iloc[1,1:] = 'Creating Logs'
        monitor.iloc[2,1:] = 'Almost Finished'    
        if verbose:
            if html_param:
                update_display(monitor, display_id = 'monitor')

        with mlflow.start_run(run_name='Stacking Regressor') as run:   

            # Get active run to log as tag
            RunID = mlflow.active_run().info.run_id

            params = model.get_params()

            for i in list(params):
                v = params.get(i)
                if len(str(v)) > 250:
                    params.pop(i)
            
            try:
                mlflow.log_params(params)
            except:
                pass
            
            mlflow.log_metrics({"MAE": avgs_mae[0], "MSE": avgs_mse[0], "RMSE": avgs_rmse[0], "R2" : avgs_r2[0],
                                "RMSLE": avgs_rmsle[0], "MAPE": avgs_mape[0]})
            
            #set tag of stack_models
            mlflow.set_tag("Source", "stack_models")
            
            import secrets
            URI = secrets.token_hex(nbytes=4)
            mlflow.set_tag("URI", URI)
            mlflow.set_tag("USI", USI)
            mlflow.set_tag("Run Time", runtime)
            mlflow.set_tag("Run ID", RunID)

            # Log training time of compare_models
            mlflow.log_metric("TT", model_fit_time)

            # Log the CV results as model_results.html artifact
            model_results.data.to_html('Results.html', col_space=65, justify='left')
            mlflow.log_artifact('Results.html')
            os.remove('Results.html')

            # Generate hold-out predictions and save as html
            holdout = predict_model(model, verbose=False)
            holdout_score = pull()
            del(holdout)
            display_container.pop(-1)
            holdout_score.to_html('Holdout.html', col_space=65, justify='left')
            mlflow.log_artifact('Holdout.html')
            os.remove('Holdout.html')

            # Log AUC and Confusion Matrix plot
            if log_plots_param:

                logger.info("SubProcess plot_model() called ==================================")

                try:
                    plot_model(model, plot = 'residuals', verbose=False, save=True, system=False)
                    mlflow.log_artifact('Residuals.png')
                    os.remove("Residuals.png")
                except:
                    pass

                try:
                    plot_model(model, plot = 'error', verbose=False, save=True, system=False)
                    mlflow.log_artifact('Prediction Error.png')
                    os.remove("Prediction Error.png")
                except:
                    pass

                try:
                    plot_model(model, plot = 'feature', verbose=False, save=True, system=False)
                    mlflow.log_artifact('Feature Importance.png')
                    os.remove("Feature Importance.png")
                except:
                    pass

                logger.info("SubProcess plot_model() end ==================================")

            # Log model and transformation pipeline
            from copy import deepcopy

            # get default conda env
            from mlflow.sklearn import get_default_conda_env
            default_conda_env = get_default_conda_env()
            default_conda_env['name'] = str(exp_name_log) + '-env'
            default_conda_env.get('dependencies').pop(-3)
            dependencies = default_conda_env.get('dependencies')[-1]
            from pycaret.utils import __version__
            dep = 'pycaret==' + str(__version__())
            dependencies['pip'] = [dep]
            
            # define model signature
            from mlflow.models.signature import infer_signature
            signature = infer_signature(data_before_preprocess.drop([target_param], axis=1))
            input_example = data_before_preprocess.drop([target_param], axis=1).iloc[0].to_dict()

            # log model as sklearn flavor
            prep_pipe_temp = deepcopy(prep_pipe)
            prep_pipe_temp.steps.append(['trained model', model])
            mlflow.sklearn.log_model(prep_pipe_temp, "model", conda_env = default_conda_env, signature = signature, input_example = input_example)
            del(prep_pipe_temp)

    if verbose:
        clear_output()
        if html_param:
            display(model_results)
        else:
            print(model_results.data)

    progress.value += 1
    
    logger.info("create_model_container: " + str(len(create_model_container)))
    logger.info("master_model_container: " + str(len(master_model_container)))
    logger.info("display_container: " + str(len(display_container)))

    logger.info(str(model))
    logger.info("stack_models() succesfully completed......................................")

    return model

def plot_model(estimator, 
               plot = 'residuals',
               save = False, #added in pycaret 1.0.1
               verbose = True, #added in pycaret 1.0.1
               system = True): #added in pycaret 1.0.1): 
    
    
    """
    This function takes a trained model object and returns a plot based on the
    test / hold-out set. The process may require the model to be re-trained in
    certain cases. See list of plots supported below. 
    
    Model must be created using create_model() or tune_model().

    Example
    --------
    >>> from pycaret.datasets import get_data
    >>> boston = get_data('boston')
    >>> experiment_name = setup(data = boston,  target = 'medv')
    >>> lr = create_model('lr')
    >>> plot_model(lr)

    This will return an residuals plot of a trained Linear Regression model.

    Parameters
    ----------
    estimator : object, default = none
        A trained model object should be passed as an estimator. 
   
    plot : string, default = residual
        Enter abbreviation of type of plot. The current list of plots supported are (Plot - Name):

        * 'residuals' - Residuals Plot
        * 'error' - Prediction Error Plot
        * 'cooks' - Cooks Distance Plot                         
        * 'rfe' - Recursive Feat. Selection                     
        * 'learning' - Learning Curve                           
        * 'vc' - Validation Curve                               
        * 'manifold' - Manifold Learning                        
        * 'feature' - Feature Importance                        
        * 'parameter' - Model Hyperparameter                    

    save: Boolean, default = False
        When set to True, Plot is saved as a 'png' file in current working directory.

    verbose: Boolean, default = True
        Progress bar not shown when verbose set to False. 

    system: Boolean, default = True
        Must remain True all times. Only to be changed by internal functions.


    Returns
    -------
    Visual_Plot
        Prints the visual plot. 

    """  
    
    
    '''
    
    ERROR HANDLING STARTS HERE
    
    '''
    
    #exception checking   
    import sys

    import logging

    try:
        hasattr(logger, 'name')
    except:
        logger = logging.getLogger('logs')
        logger.setLevel(logging.DEBUG)
        
        # create console handler and set level to debug
        if logger.hasHandlers():
            logger.handlers.clear()
        
        ch = logging.FileHandler('logs.log')
        ch.setLevel(logging.DEBUG)

        # create formatter
        formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        logger.addHandler(ch)

    logger.info("Initializing plot_model()")
    logger.info("""plot_model(estimator={}, plot={}, save={}, verbose={}, system={})""".\
        format(str(estimator), str(plot), str(save), str(verbose), str(system)))
    
    logger.info("Checking exceptions")

    #checking plots (string)
    available_plots = ['residuals', 'error', 'cooks', 'feature', 'parameter', 'rfe', 'learning', 'manifold', 'vc']
    
    if plot not in available_plots:
        sys.exit('(Value Error): Plot Not Available. Please see docstring for list of available Plots.')

    #exception for CatBoost
    if 'CatBoostRegressor' in str(type(estimator)):
        sys.exit('(Estimator Error): CatBoost estimator is not compatible with plot_model function, try using Catboost with interpret_model instead.')
        
    #checking for feature plot
    if not ( hasattr(estimator, 'coef_') or hasattr(estimator,'feature_importances_') ) and (plot == 'feature' or plot == 'rfe'):
        sys.exit('(Type Error): Feature Importance plot not available for estimators with coef_ attribute.')
    
    '''
    
    ERROR HANDLING ENDS HERE
    
    '''
    
    logger.info("Preloading libraries")
    #pre-load libraries
    import pandas as pd
    import ipywidgets as ipw
    from IPython.display import display, HTML, clear_output, update_display
    from copy import deepcopy
    
    logger.info("Preparing display monitor")
    #progress bar
    progress = ipw.IntProgress(value=0, min=0, max=5, step=1 , description='Processing: ')
    if verbose:
        if html_param:
            display(progress)
    
    #ignore warnings
    import warnings
    warnings.filterwarnings('ignore') 
    
    logger.info("Importing libraries")
    #general dependencies
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    from sklearn.base import clone
    
    #defining estimator as model locally
    model = estimator
    
    progress.value += 1
    
    #plots used for logging (controlled through plots_log_param) 
    #residuals, #error, and #feature importance

    logger.info("plot type: " + str(plot)) 

    if plot == 'residuals':
        
        from yellowbrick.regressor import ResidualsPlot
        progress.value += 1
        visualizer = ResidualsPlot(model)
        logger.info("Fitting Model")
        visualizer.fit(X_train, y_train)
        progress.value += 1
        logger.info("Scoring test/hold-out set")
        visualizer.score(X_test, y_test)  # Evaluate the model on the test data
        progress.value += 1
        clear_output()
        if save:
            logger.info("Saving 'Residuals.png' in current active directory")
            if system:
                visualizer.show(outpath="Residuals.png")
            else:
                visualizer.show(outpath="Residuals.png", clear_figure=True)
        else:
            visualizer.show()
        
        logger.info("Visual Rendered Successfully")
        
    elif plot == 'error':
        from yellowbrick.regressor import PredictionError
        progress.value += 1
        visualizer = PredictionError(model)
        logger.info("Fitting Model")
        visualizer.fit(X_train, y_train)
        progress.value += 1
        logger.info("Scoring test/hold-out set")
        visualizer.score(X_test, y_test)
        progress.value += 1
        clear_output()
        if save:
            logger.info("Saving 'Prediction Error.png' in current active directory")
            if system:
                visualizer.show(outpath="Prediction Error.png")
            else:
                visualizer.show(outpath="Prediction Error.png", clear_figure=True)
        else:
            visualizer.show()
        
        logger.info("Visual Rendered Successfully")

    elif plot == 'cooks':
        from yellowbrick.regressor import CooksDistance
        progress.value += 1
        visualizer = CooksDistance()
        progress.value += 1
        logger.info("Fitting Model")
        visualizer.fit(X, y)
        progress.value += 1
        clear_output()
        if save:
            logger.info("Saving 'Cooks Distance.png' in current active directory")
            if system:
                visualizer.show(outpath="Cooks Distance.png")
            else:
                visualizer.show(outpath="Cooks Distance.png", clear_figure=True)
        else:
            visualizer.show()
        
        logger.info("Visual Rendered Successfully")

    elif plot == 'rfe':
        
        from yellowbrick.model_selection import RFECV 
        progress.value += 1
        visualizer = RFECV(model, cv=10)
        progress.value += 1
        logger.info("Fitting Model")
        visualizer.fit(X_train, y_train)
        progress.value += 1
        clear_output()
        if save:
            logger.info("Saving 'Recursive Feature Selection.png' in current active directory")
            if system:
                visualizer.show(outpath="Recursive Feature Selection.png")
            else:
                visualizer.show(outpath="Recursive Feature Selection.png", clear_figure=True)
        else:
            visualizer.show()
        
        logger.info("Visual Rendered Successfully")

    elif plot == 'learning':
        
        from yellowbrick.model_selection import LearningCurve
        progress.value += 1
        sizes = np.linspace(0.3, 1.0, 10)  
        visualizer = LearningCurve(model, cv=10, train_sizes=sizes, n_jobs=1, random_state=seed)
        progress.value += 1
        logger.info("Fitting Model")
        visualizer.fit(X_train, y_train)
        progress.value += 1
        clear_output()
        if save:
            logger.info("Saving 'Learning Curve.png' in current active directory")
            if system:
                visualizer.show(outpath="Learning Curve.png")
            else:
                visualizer.show(outpath="Learning Curve.png", clear_figure=True)
        else:
            visualizer.show()

        logger.info("Visual Rendered Successfully")

    elif plot == 'manifold':
        
        from yellowbrick.features import Manifold
        
        progress.value += 1
        X_train_transformed = X_train.select_dtypes(include='float64') 
        visualizer = Manifold(manifold='tsne', random_state = seed)
        progress.value += 1
        logger.info("Fitting Model")
        visualizer.fit_transform(X_train_transformed, y_train)
        progress.value += 1
        clear_output()
        if save:
            logger.info("Saving 'Manifold.png' in current active directory")
            if system:
                visualizer.show(outpath="Manifold.png")
            else:
                visualizer.show(outpath="Manifold.png", clear_figure=True)
        else:
            visualizer.show()

        logger.info("Visual Rendered Successfully")

    elif plot == 'vc':
        
        model_name = str(model).split("(")[0]
        
        not_allowed = ['LinearRegression', 'PassiveAggressiveRegressor']
        
        logger.info("Determining param_name")

        if model_name in not_allowed:
            clear_output()
            sys.exit('(Value Error): Estimator not supported in Validation Curve Plot.')
        
        elif model_name == 'GradientBoostingRegressor':
            param_name='alpha'
            param_range = np.arange(0.1,1,0.1)
        
        #lasso/ridge/en/llar/huber/kr/mlp/br/ard
        elif hasattr(model, 'alpha'):
            param_name='alpha'
            param_range = np.arange(0,1,0.1)
            
        elif hasattr(model, 'alpha_1'):
            param_name='alpha_1'
            param_range = np.arange(0,1,0.1)
            
        #par/svm
        elif hasattr(model, 'C'):
            param_name='C'
            param_range = np.arange(1,11)
            
        #tree based models (dt/rf/et)
        elif hasattr(model, 'max_depth'):
            param_name='max_depth'
            param_range = np.arange(1,11)
        
        #knn
        elif hasattr(model, 'n_neighbors'):
            param_name='n_neighbors'
            param_range = np.arange(1,11)         
            
        #Bagging / Boosting (ada/gbr)
        elif hasattr(model, 'n_estimators'):
            param_name='n_estimators'
            param_range = np.arange(1,100,10)   

        #Bagging / Boosting (ada/gbr)
        elif hasattr(model, 'n_nonzero_coefs'):
            param_name='n_nonzero_coefs'
            if len(X_train.columns) >= 10:
                param_max = 11
            else:
                param_max = len(X_train.columns)+1
            param_range = np.arange(1,param_max,1) 
            
        elif hasattr(model, 'eps'):
            param_name='eps'
            param_range = np.arange(0,1,0.1)   
            
        elif hasattr(model, 'max_subpopulation'):
            param_name='max_subpopulation'
            param_range = np.arange(1000,20000,2000)   

        elif hasattr(model, 'min_samples'):
            param_name='min_samples'
            param_range = np.arange(0.01,1,0.1)  
            
        else: 
            clear_output()
            sys.exit('(Value Error): Estimator not supported in Validation Curve Plot.')
        
        logger.info("param_name: " + str(param_name))

        progress.value += 1
            
        from yellowbrick.model_selection import ValidationCurve
        viz = ValidationCurve(model, param_name=param_name, param_range=param_range,cv=10, 
                              random_state=seed)
        logger.info("Fitting Model")
        viz.fit(X_train, y_train)
        progress.value += 1
        clear_output()
        if save:
            logger.info("Saving 'Validation Curve.png' in current active directory")
            if system:
                viz.show(outpath="Validation Curve.png")
            else:
                viz.show(outpath="Validation Curve.png", clear_figure=True)
        else:
            viz.show()
        
        logger.info("Visual Rendered Successfully")

    elif plot == 'feature':
        if hasattr(estimator, 'coef_'):
            try:
                variables = abs(model.coef_)
            except:
                logger.warning("No coef_ found. Trying feature_importances_")
                variables = abs(model.feature_importances_)
        else:
            variables = abs(model.feature_importances_)
        col_names = np.array(X_train.columns)
        coef_df = pd.DataFrame({'Variable': X_train.columns, 'Value': variables})
        progress.value += 1
        sorted_df = coef_df.sort_values(by='Value', ascending=False)
        sorted_df = sorted_df.head(10)
        sorted_df = sorted_df.sort_values(by='Value')
        my_range=range(1,len(sorted_df.index)+1)
        plt.figure(figsize=(8,5))
        plt.hlines(y=my_range, xmin=0, xmax=sorted_df['Value'], color='skyblue')
        plt.plot(sorted_df['Value'], my_range, "o")
        plt.yticks(my_range, sorted_df['Variable'])
        progress.value += 1
        plt.title("Feature Importance Plot")
        plt.xlabel('Variable Importance')
        plt.ylabel('Features') 
        progress.value += 1
        clear_output()
        if save:
            logger.info("Saving 'Feature Importance.png' in current active directory")
            if system:
                plt.savefig("Feature Importance.png")
            else:
                plt.savefig("Feature Importance.png")
                plt.close()
        else:
            plt.show()

        logger.info("Visual Rendered Successfully")

    elif plot == 'parameter':
        
        clear_output()
        param_df = pd.DataFrame.from_dict(estimator.get_params(estimator), orient='index', columns=['Parameters'])
        display(param_df)

        logger.info("Visual Rendered Successfully")
    
    logger.info("plot_model() succesfully completed......................................")

def evaluate_model(estimator):
    
    
    """
    This function displays a user interface for all of the available plots for 
    a given estimator. It internally uses the plot_model() function. 
    
    Example
    --------
    >>> from pycaret.datasets import get_data
    >>> boston = get_data('boston')
    >>> experiment_name = setup(data = boston,  target = 'medv')
    >>> lr = create_model('lr')
    >>> evaluate_model(lr)
    
    This will display the User Interface for all of the plots for a given
    estimator.

    Parameters
    ----------
    estimator : object, default = none
        A trained model object should be passed as an estimator. 

    Returns
    -------
    User_Interface
        Displays the user interface for plotting.    

    """
        
        
    from ipywidgets import widgets
    from ipywidgets.widgets import interact, fixed, interact_manual

    a = widgets.ToggleButtons(
                            options=[('Hyperparameters', 'parameter'),
                                     ('Residuals Plot', 'residuals'), 
                                     ('Prediction Error Plot', 'error'), 
                                     ('Cooks Distance Plot', 'cooks'),
                                     ('Recursive Feature Selection', 'rfe'),
                                     ('Learning Curve', 'learning'),
                                     ('Validation Curve', 'vc'),
                                     ('Manifold Learning', 'manifold'),
                                     ('Feature Importance', 'feature')
                                    ],

                            description='Plot Type:',

                            disabled=False,

                            button_style='', # 'success', 'info', 'warning', 'danger' or ''

                            icons=['']
    )
    
  
    d = interact(plot_model, estimator = fixed(estimator), plot = a, save = fixed(False), verbose = fixed(True), system = fixed(True))

def interpret_model(estimator,
                   plot = 'summary',
                   feature = None, 
                   observation = None):
    
    
    """
    This function takes a trained model object and returns an interpretation plot 
    based on the test / hold-out set. It only supports tree based algorithms. 

    This function is implemented based on the SHAP (SHapley Additive exPlanations),
    which is a unified approach to explain the output of any machine learning model. 
    SHAP connects game theory with local explanations.

    For more information : https://shap.readthedocs.io/en/latest/

    Example
    --------
    >>> from pycaret.datasets import get_data
    >>> boston = get_data('boston')
    >>> experiment_name = setup(data = boston,  target = 'medv')
    >>> dt = create_model('dt')
    >>> interpret_model(dt)

    This will return a summary interpretation plot of Decision Tree model.

    Parameters
    ----------
    estimator : object, default = none
        A trained tree based model object should be passed as an estimator. 

    plot : string, default = 'summary'
        Other available options are 'correlation' and 'reason'.

    feature: string, default = None
        This parameter is only needed when plot = 'correlation'. By default feature is 
        set to None which means the first column of the dataset will be used as a variable. 
        A feature parameter must be passed to change this.

    observation: integer, default = None
        This parameter only comes into effect when plot is set to 'reason'. If no observation
        number is provided, it will return an analysis of all observations with the option
        to select the feature on x and y axes through drop down interactivity. For analysis at
        the sample level, an observation parameter must be passed with the index value of the
        observation in test / hold-out set. 

    Returns
    -------
    Visual_Plot
        Returns the visual plot.
        Returns the interactive JS plot when plot = 'reason'.

    """
    
    
    
    '''
    Error Checking starts here
    
    '''
    
    import sys
    import logging

    try:
        hasattr(logger, 'name')
    except:
        logger = logging.getLogger('logs')
        logger.setLevel(logging.DEBUG)
        
        # create console handler and set level to debug
        if logger.hasHandlers():
            logger.handlers.clear()
        
        ch = logging.FileHandler('logs.log')
        ch.setLevel(logging.DEBUG)

        # create formatter
        formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        logger.addHandler(ch)

    logger.info("Initializing interpret_model()")
    logger.info("""interpret_model(estimator={}, plot={}, feature={}, observation={})""".\
        format(str(estimator), str(plot), str(feature), str(observation)))

    logger.info("Checking exceptions")

    #checking if shap available
    try:
        import shap
    except:
        logger.error("shap library not found. pip install shap to use interpret_model function.")
        sys.exit("shap library not found. pip install shap to use interpret_model function.")  
        
    #allowed models
    allowed_models = ['RandomForestRegressor',
                      'DecisionTreeRegressor',
                      'ExtraTreesRegressor',
                      'GradientBoostingRegressor',
                      'XGBRegressor',
                      'LGBMRegressor',
                      'CatBoostRegressor']
    
    model_name = str(estimator).split("(")[0]

    #Statement to find CatBoost and change name :
    if model_name.find("catboost.core.CatBoostRegressor") != -1:
        model_name = 'CatBoostRegressor'
    
    if model_name not in allowed_models:
        sys.exit('(Type Error): This function only supports tree based models.')
        
    #plot type
    allowed_types = ['summary', 'correlation', 'reason']
    if plot not in allowed_types:
        sys.exit("(Value Error): type parameter only accepts 'summary', 'correlation' or 'reason'.")   
           
    
    '''
    Error Checking Ends here
    
    '''
        
    logger.info("Importing libraries")
    #general dependencies
    import numpy as np
    import pandas as pd
    import shap
    
    #storing estimator in model variable
    model = estimator
    
    if plot == 'summary':

        logger.info("plot type: summary")
        logger.info("Creating TreeExplainer")
        explainer = shap.TreeExplainer(model)
        logger.info("Compiling shap values")
        shap_values = explainer.shap_values(X_test)
        shap.summary_plot(shap_values, X_test)
        logger.info("Visual Rendered Successfully")
                              
    elif plot == 'correlation':

        logger.info("plot type: correlation")
        
        if feature == None:
            logger.warning("No feature passed. Default value of feature used for correlation plot: " + str(X_test.columns[0]))
            dependence = X_test.columns[0]
            
        else:
            logger.warning("feature value passed. Feature used for correlation plot: " + str(X_test.columns[0]))
            dependence = feature
        
        logger.info("Creating TreeExplainer")
        explainer = shap.TreeExplainer(model)
        logger.info("Compiling shap values")
        shap_values = explainer.shap_values(X_test) 
        shap.dependence_plot(dependence, shap_values, X_test)
        logger.info("Visual Rendered Successfully")
        
    elif plot == 'reason':
        logger.info("plot type: reason")
     
        if observation is None:
            logger.warning("Observation set to None. Model agnostic plot will be rendered.")
            logger.info("Creating TreeExplainer")
            explainer = shap.TreeExplainer(model)
            logger.info("Compiling shap values")
            shap_values = explainer.shap_values(X_test)
            shap.initjs()
            logger.info("Visual Rendered Successfully")
            logger.info("interpret_model() succesfully completed......................................")
            return shap.force_plot(explainer.expected_value, shap_values, X_test)

        else:

            row_to_show = observation
            data_for_prediction = X_test.iloc[row_to_show]
            logger.info("Creating TreeExplainer")
            explainer = shap.TreeExplainer(model)
            logger.info("Compiling shap values")
            shap_values = explainer.shap_values(X_test)
            shap.initjs()
            logger.info("Visual Rendered Successfully")
            logger.info("interpret_model() succesfully completed......................................")
            return shap.force_plot(explainer.expected_value, shap_values[row_to_show,:], X_test.iloc[row_to_show,:])

    logger.info("interpret_model() succesfully completed......................................")

def predict_model(estimator, 
                  data=None,
                  round=4,
                  verbose=True): #added in pycaret==2.0.0
    
    """
       
    Description:
    ------------
    This function is used to predict target value on the new dataset using a trained 
    estimator. New unseen data can be passed to data param as pandas.DataFrame.
    If data is not passed, the test / hold-out set separated at the time of 
    setup() is used to generate predictions. 
    
        Example:
        --------
        from pycaret.datasets import get_data
        boston = get_data('boston')
        experiment_name = setup(data = boston,  target = 'medv')
        lr = create_model('lr')
        
        lr_predictions_holdout = predict_model(lr)
        
    Parameters
    ----------
    estimator : object, default = none
        A trained model object / pipeline should be passed as an estimator. 
    
    data : pandas.DataFrame
        shape (n_samples, n_features) where n_samples is the number of samples and n_features is the number of features.
        All features used during training must be present in the new dataset.
    
    round: integer, default = 4
        Number of decimal places the predicted labels will be rounded to.
    
    verbose: Boolean, default = True
        Holdout score grid is not printed when verbose is set to False.

    Returns
    -------
    
    Predictions:  Predictions (Label and Score) column attached to the original dataset
    -----------   and returned as pandas.DataFrame.

    score grid:   A table containing the scoring metrics on hold-out / test set.
    -----------              
    
    """
    
    # ignore warnings
    import warnings
    warnings.filterwarnings('ignore') 

    # general dependencies
    import sys
    import numpy as np
    import pandas as pd
    import re
    from sklearn import metrics
    from copy import deepcopy
    from IPython.display import clear_output, update_display, display
    
    def calculate_mape(actual, prediction):
        mask = actual != 0
        return (np.fabs(actual - prediction)/actual)[mask].mean()
        
    # retrieve target transformation
    try:
        target_transformer = target_inverse_transformer
    except:
        target_transformer = estimator.steps[13][1].p_transform_target # make it dynamic instead of hardcoding no 13
            
    # dataset
    if data is None:
        
        if 'Pipeline' in str(type(estimator)):
            estimator = estimator[-1]

        Xtest = X_test.copy()
        ytest = y_test.copy()
        X_test_ = X_test.copy()
        y_test_ = y_test.copy()
        
        index = None
        Xtest.reset_index(drop=True, inplace=True)
        ytest.reset_index(drop=True, inplace=True)
        X_test_.reset_index(drop=True, inplace=True)
        y_test_.reset_index(drop=True, inplace=True)

    else:
        
        if 'Pipeline' in str(type(estimator)):
            pass
        else:
            try:
                estimator_ = deepcopy(prep_pipe)
                estimator_.steps.append(['trained model',estimator])
                estimator = estimator_
                del(estimator_)

            except:
                sys.exit("Pipeline not found")
            
        Xtest = data.copy()
        X_test_ = data.copy()
        Xtest.reset_index(drop=True, inplace=True)
        X_test_.reset_index(inplace=True)

        index = X_test_['index']
        X_test_.drop('index', axis=1, inplace=True)

    # model name
    full_name = str(estimator).split("(")[0]
    def putSpace(input):
        words = re.findall('[A-Z][a-z]*', input)
        words = ' '.join(words)
        return words  
    full_name = putSpace(full_name)

    if full_name == 'A R D Regression':
        full_name = 'Automatic Relevance Determination'

    elif full_name == 'M L P Regressor':
        full_name = 'MLP Regressor'

    elif full_name == 'R A N S A C Regressor':
        full_name = 'RANSAC Regressor'

    elif full_name == 'S V R':
        full_name = 'Support Vector Regressor'
        
    elif full_name == 'Lars':
        full_name = 'Least Angle Regression'
        
    elif full_name == 'X G B Regressor':
        full_name = 'Extreme Gradient Boosting Regressor'

    elif full_name == 'L G B M Regressor':
        full_name = 'Light Gradient Boosting Machine'

    elif 'Cat Boost Regressor' in full_name:
        full_name = 'CatBoost Regressor'

    # prediction starts here
    pred_ = estimator.predict(Xtest)

    try:
        pred_ = target_transformer.inverse_transform(np.array(pred_).reshape(-1,1))
        pred_ = np.nan_to_num(pred_)

    except:
        pred_ = np.nan_to_num(pred_)
        
    if data is None:
        
        try:
            ytest = target_transformer.inverse_transform(np.array(ytest).reshape(-1,1))
            ytest = pd.DataFrame(np.nan_to_num(ytest))

        except:
            pass

        mae = metrics.mean_absolute_error(ytest,pred_)
        mse = metrics.mean_squared_error(ytest,pred_)
        rmse = np.sqrt(mse)
        rmsle = np.sqrt(np.mean(np.power(np.log(np.array(abs(pred_))+1) - np.log(np.array(abs(ytest))+1), 2)))
        r2 = metrics.r2_score(ytest,pred_)
        mape = calculate_mape(ytest,pred_)
                    
        df_score = pd.DataFrame( {'Model' : [full_name], 'MAE' : [mae], 'MSE' : [mse], 'RMSE' : [rmse], 
                                    'R2' : [r2], 'RMSLE' : [rmsle], 'MAPE' : mape })
        df_score = df_score.round(4)

        if verbose:
            display(df_score)
    
        label = pd.DataFrame(pred_)
        label = label.round(round)
        label.columns = ['Label']
        label['Label']=label['Label']

    label = pd.DataFrame(pred_)
    label = label.round(round)
    label.columns = ['Label']
    label['Label']=label['Label']
    
    if data is None:
        X_test_ = pd.concat([Xtest,ytest,label], axis=1)
    else:
        X_test_ = pd.concat([X_test_,label], axis=1)

    # store predictions on hold-out in display_container
    try:
        display_container.append(df_score)
    except:
        pass

    if index is not None:
        X_test_['index'] = index
        X_test_.set_index('index', drop=True, inplace=True)

    return X_test_

def finalize_model(estimator):
    
    """
    This function fits the estimator onto the complete dataset passed during the
    setup() stage. The purpose of this function is to prepare for final model
    deployment after experimentation. 
    
    Example
    --------
    >>> from pycaret.datasets import get_data
    >>> boston = get_data('boston')
    >>> experiment_name = setup(data = boston,  target = 'medv')
    >>> lr = create_model('lr')
    >>> final_lr = finalize_model(lr)
    
    This will return the final model object fitted to complete dataset. 

    Parameters
    ----------
    estimator : object, default = none
        A trained model object should be passed as an estimator. 

    Returns
    -------
    model
        Trained model object fitted on complete dataset.

    Warnings
    --------
    - If the model returned by finalize_model(), is used on predict_model() without 
      passing a new unseen dataset, then the information grid printed is misleading 
      as the model is trained on the complete dataset including test / hold-out sample. 
      Once finalize_model() is used, the model is considered ready for deployment and
      should be used on new unseens dataset only.
       
         
    """
    
    import logging

    try:
        hasattr(logger, 'name')
    except:
        logger = logging.getLogger('logs')
        logger.setLevel(logging.DEBUG)
        
        # create console handler and set level to debug
        if logger.hasHandlers():
            logger.handlers.clear()
        
        ch = logging.FileHandler('logs.log')
        ch.setLevel(logging.DEBUG)

        # create formatter
        formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        logger.addHandler(ch)

    logger.info("Initializing finalize_model()")
    logger.info("""finalize_model(estimator={})""".\
        format(str(estimator)))

    #ignore warnings
    import warnings
    warnings.filterwarnings('ignore') 
    
    #run_time
    import datetime, time
    runtime_start = time.time()

    logger.info("Importing libraries")
    #import depedencies
    from IPython.display import clear_output, update_display
    from sklearn.base import clone
    from copy import deepcopy
    import numpy as np

    logger.info("Getting model name")

    #determine runname for logging
    def get_model_name(e):
        return str(e).split("(")[0]
    
    model_dict_logging = {'ExtraTreesRegressor' : 'Extra Trees Regressor',
                        'GradientBoostingRegressor' : 'Gradient Boosting Regressor', 
                        'RandomForestRegressor' : 'Random Forest',
                        'LGBMRegressor' : 'Light Gradient Boosting Machine',
                        'XGBRegressor' : 'Extreme Gradient Boosting',
                        'AdaBoostRegressor' : 'AdaBoost Regressor', 
                        'DecisionTreeRegressor' : 'Decision Tree', 
                        'Ridge' : 'Ridge Regression',
                        'TheilSenRegressor' : 'TheilSen Regressor', 
                        'BayesianRidge' : 'Bayesian Ridge',
                        'LinearRegression' : 'Linear Regression',
                        'ARDRegression' : 'Automatic Relevance Determination', 
                        'KernelRidge' : 'Kernel Ridge', 
                        'RANSACRegressor' : 'Random Sample Consensus', 
                        'HuberRegressor' : 'Huber Regressor', 
                        'Lasso' : 'Lasso Regression', 
                        'ElasticNet' : 'Elastic Net', 
                        'Lars' : 'Least Angle Regression', 
                        'OrthogonalMatchingPursuit' : 'Orthogonal Matching Pursuit', 
                        'MLPRegressor' : 'Multi Level Perceptron',
                        'KNeighborsRegressor' : 'K Neighbors Regressor',
                        'SVR' : 'Support Vector Machine',
                        'LassoLars' : 'Lasso Least Angle Regression',
                        'PassiveAggressiveRegressor' : 'Passive Aggressive Regressor',
                        'CatBoostRegressor' : 'CatBoost Regressor',
                        'BaggingRegressor' : 'Bagging Regressor',
                        'VotingRegressor' : 'Voting Regressor',
                        'StackingRegressor' : 'Stacking Regressor'}
                            
    

    if hasattr(estimator, 'voting'):
        mn = 'VotingRegressor'
    else:
        mn = get_model_name(estimator)

    if 'BaggingRegressor' in mn:
        mn = get_model_name(estimator.base_estimator_)

    if 'catboost' in mn:
        mn = 'CatBoostRegressor'

    full_name = model_dict_logging.get(mn)

    logger.info("Finalizing " + str(full_name))
    model_final = clone(estimator)
    clear_output()
    model_final.fit(X,y)
    model = create_model(estimator=estimator, verbose=False, system=False)
    results = pull()
    
    #end runtime
    runtime_end = time.time()
    runtime = np.array(runtime_end - runtime_start).round(2)

    #mlflow logging
    if logging_param:

        logger.info("Creating MLFlow logs")

        #import mlflow
        import mlflow
        from pathlib import Path
        import os

        mlflow.set_experiment(exp_name_log)

        with mlflow.start_run(run_name=full_name) as run:

            # Get active run to log as tag
            RunID = mlflow.active_run().info.run_id

            # Log metrics
            mlflow.log_metrics({"MAE": results.iloc[-2]['MAE'], "MSE": results.iloc[-2]['MSE'], "RMSE": results.iloc[-2]['RMSE'], "R2" : results.iloc[-2]['R2'],
                                "RMSLE": results.iloc[-2]['RMSLE'], "MAPE": results.iloc[-2]['MAPE']})

            #set tag of compare_models
            mlflow.set_tag("Source", "finalize_model")
            
            #create MRI (model registration id)
            mlflow.set_tag("Final", True)
            
            import secrets
            URI = secrets.token_hex(nbytes=4)
            mlflow.set_tag("URI", URI)           
            mlflow.set_tag("USI", USI)
            mlflow.set_tag("Run Time", runtime)
            mlflow.set_tag("Run ID", RunID)

            # Log training time in seconds
            mlflow.log_metric("TT", runtime)

            # Log AUC and Confusion Matrix plot
            if log_plots_param:

                logger.info("SubProcess plot_model() called ==================================")

                try:
                    plot_model(model_final, plot = 'residuals', verbose=False, save=True, system=False)
                    mlflow.log_artifact('Residuals.png')
                    os.remove("Residuals.png")
                except:
                    pass

                try:
                    plot_model(model_final, plot = 'error', verbose=False, save=True, system=False)
                    mlflow.log_artifact('Prediction Error.png')
                    os.remove("Prediction Error.png")
                except:
                    pass

                try:
                    plot_model(model_final, plot = 'feature', verbose=False, save=True, system=False)
                    mlflow.log_artifact('Feature Importance.png')
                    os.remove("Feature Importance.png")
                except:
                    pass

                logger.info("SubProcess plot_model() end ==================================")

            # Log model and transformation pipeline
            from copy import deepcopy

            # get default conda env
            from mlflow.sklearn import get_default_conda_env
            default_conda_env = get_default_conda_env()
            default_conda_env['name'] = str(exp_name_log) + '-env'
            default_conda_env.get('dependencies').pop(-3)
            dependencies = default_conda_env.get('dependencies')[-1]
            from pycaret.utils import __version__
            dep = 'pycaret==' + str(__version__())
            dependencies['pip'] = [dep]
            
            # define model signature
            from mlflow.models.signature import infer_signature
            signature = infer_signature(data_before_preprocess)

            # log model as sklearn flavor
            prep_pipe_temp = deepcopy(prep_pipe)
            prep_pipe_temp.steps.append(['trained model', model_final])
            mlflow.sklearn.log_model(prep_pipe_temp, "model", conda_env = default_conda_env, signature = signature)
            del(prep_pipe_temp)

    logger.info("create_model_container: " + str(len(create_model_container)))
    logger.info("master_model_container: " + str(len(master_model_container)))
    logger.info("display_container: " + str(len(display_container)))

    logger.info(str(model_final))

    logger.info("finalize_model() succesfully completed......................................")

    return model_final

def deploy_model(model,
                 model_name,
                 authentication,
                 platform='aws'):
    """
    (In Preview)

    This function deploys the transformation pipeline and trained model object for
    production use. The platform of deployment can be defined under the platform
    param along with the applicable authentication tokens which are passed as a
    dictionary to the authentication param.

    Example
    -------
    >>> from pycaret.datasets import get_data
    >>> juice = get_data('juice')
    >>> experiment_name = setup(data = juice,  target = 'Purchase')
    >>> lr = create_model('lr')
    >>> deploy_model(model = lr, model_name = 'deploy_lr', platform = 'aws', authentication = {'bucket' : 'pycaret-test'})

    This will deploy the model on an AWS S3 account under bucket 'pycaret-test'

    Notes
    -----
    For AWS users:
    Before deploying a model to an AWS S3 ('aws'), environment variables must be
    configured using the command line interface. To configure AWS env. variables,
    type aws configure in your python command line. The following information is
    required which can be generated using the Identity and Access Management (IAM)
    portal of your amazon console account:

    - AWS Access Key ID
    - AWS Secret Key Access
    - Default Region Name (can be seen under Global settings on your AWS console)
    - Default output format (must be left blank)

    For GCP users:
    --------------
    Before deploying a model to Google Cloud Platform (GCP), user has to create Project
    on the platform from consol. To do that, user must have google cloud account or
    create new one. After creating a service account, down the JSON authetication file
    and configure  GOOGLE_APPLICATION_CREDENTIALS= <path-to-json> from command line. If
    using google-colab then authetication can be done using `google.colab` auth method.
    Read below link for more details.

    https://cloud.google.com/docs/authentication/production

    - Google Cloud Project
    - Service Account Authetication

    For AZURE users:
    --------------
    Before deploying a model to Microsoft's Azure (Azure), environment variables
    for connection string must be set. In order to get connection string, user has
    to create account of Azure. Once it is done, create a Storage account. In the settings
    section of storage account, user can get the connection string.

    Read below link for more details.
    https://docs.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python?toc=%2Fpython%2Fazure%2FTOC.json

    - Azure Storage Account

    Parameters
    ----------
    model : object
        A trained model object should be passed as an estimator.

    model_name : string
        Name of model to be passed as a string.

    authentication : dict
        Dictionary of applicable authentication tokens.

        When platform = 'aws':
        {'bucket' : 'Name of Bucket on S3'}

        When platform = 'gcp':
        {'project': 'gcp_pycaret', 'bucket' : 'pycaret-test'}

        When platform = 'azure':
        {'container': 'pycaret-test'}

    platform: string, default = 'aws'
        Name of platform for deployment. Current available options are: 'aws', 'gcp' and 'azure'

    Returns
    -------
    Success_Message

    Warnings
    --------
    - This function uses file storage services to deploy the model on cloud platform.
      As such, this is efficient for batch-use. Where the production objective is to
      obtain prediction at an instance level, this may not be the efficient choice as
      it transmits the binary pickle file between your local python environment and
      the platform.

    """

    import sys
    import logging

    try:
        hasattr(logger, 'name')
    except:
        logger = logging.getLogger('logs')
        logger.setLevel(logging.DEBUG)

        # create console handler and set level to debug
        if logger.hasHandlers():
            logger.handlers.clear()

        ch = logging.FileHandler('logs.log')
        ch.setLevel(logging.DEBUG)

        # create formatter
        formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        logger.addHandler(ch)

    logger.info("Initializing deploy_model()")
    logger.info("""deploy_model(model={}, model_name={}, authentication={}, platform={})""". \
                format(str(model), str(model_name), str(authentication), str(platform)))

    # checking if awscli available
    try:
        import awscli
    except:
        logger.error("awscli library not found. pip install awscli to use deploy_model function.")
        sys.exit("awscli library not found. pip install awscli to use deploy_model function.")

        # ignore warnings
    import warnings
    warnings.filterwarnings('ignore')

    # general dependencies
    import ipywidgets as ipw
    import pandas as pd
    from IPython.display import clear_output, update_display
    import os

    if platform == 'aws':

        logger.info("Platform : AWS S3")

        import boto3

        logger.info("Saving model in active working directory")
        logger.info("SubProcess save_model() called ==================================")
        save_model(model, model_name=model_name, verbose=False)
        logger.info("SubProcess save_model() end ==================================")

        # initiaze s3
        logger.info("Initializing S3 client")
        s3 = boto3.client('s3')
        filename = str(model_name) + '.pkl'
        key = str(model_name) + '.pkl'
        bucket_name = authentication.get('bucket')
        s3.upload_file(filename, bucket_name, key)
        clear_output()
        os.remove(filename)
        print("Model Succesfully Deployed on AWS S3")
        logger.info(str(model))
        logger.info("deploy_model() succesfully completed......................................")

    elif platform == 'gcp':

        try:
            import google.cloud
        except:
            logger.error(
                "google.cloud library not found. pip install google.cloud to use deploy_model function with GCP.")
            sys.exit("google.cloud library not found. pip install google.cloud to use deploy_model function with GCP.")

        save_model(model, model_name=model_name, verbose=False)
        filename = str(model_name) + '.pkl'
        key = str(model_name) + '.pkl'
        bucket_name = authentication.get('bucket')
        project_name = authentication.get('project')
        logger.info('Deploying model to Google Cloud Platform')
        # Create Bucket
        _create_bucket_gcp(project_name, bucket_name)
        _upload_blob_gcp(project_name, bucket_name, filename, key)
        logger.info('Deployed model Successfully on Google Cloud Platform')

    elif platform == 'azure':

        try:
            import azure.storage.blob
        except:
            logger.error(
                "azure.storage.blob library not found. pip install azure-storage-blob to use deploy_model function with Azure.")
            sys.exit(
                "azure.storage.blob library not found. pip install azure-storage-blob to use deploy_model function with Azure.")

        logger.info('Deploying model to Microsoft Azure')
        save_model(model, model_name=model_name, verbose=False)
        filename = str(model_name) + '.pkl'
        key = str(model_name) + '.pkl'
        container_name = authentication.get('container')
        container_client = _create_container_azure(container_name)
        _upload_blob_azure(container_name, filename, key)

    else:
        logger.error('Platform {} is not supported by pycaret or illegal option'.format(platform))
        sys.exit('Platform {} is not supported by pycaret or illegal option'.format(platform))

def save_model(model, model_name, model_only=False, verbose=True):
    
    """
    This function saves the transformation pipeline and trained model object 
    into the current active directory as a pickle file for later use. 
    

        Example:
        --------
        from pycaret.datasets import get_data
        boston = get_data('boston')
        experiment_name = setup(data = boston,  target = 'medv')
        lr = create_model('lr')

        save_model(lr, 'lr_model_23122019')

        This will save the transformation pipeline and model as a binary pickle
        file in the current directory. 


    Parameters
    ----------
    model : object, default = none
        A trained model object should be passed as an estimator. 
    
    model_name : string, default = none
        Name of pickle file to be passed as a string.
    
    model_only : bool, default = False
        When set to True, only trained model object is saved and all the 
        transformations are ignored.
   
    verbose: Boolean, default = True
        Success message is not printed when verbose is set to False.

    Returns
    --------    
    Success_Message

    """
    
    import logging
    from copy import deepcopy

    try:
        hasattr(logger, 'name')
    except:
        logger = logging.getLogger('logs')
        logger.setLevel(logging.DEBUG)
        
        # create console handler and set level to debug
        if logger.hasHandlers():
            logger.handlers.clear()
        
        ch = logging.FileHandler('logs.log')
        ch.setLevel(logging.DEBUG)

        # create formatter
        formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        logger.addHandler(ch)

    logger.info("Initializing save_model()")
    logger.info("""save_model(model={}, model_name={}, model_only={}, verbose={})""".\
        format(str(model), str(model_name), str(model_only), str(verbose)))

    #ignore warnings
    import warnings
    warnings.filterwarnings('ignore') 
    
    if model_only:
        model_ = deepcopy(model)
        logger.warning("Only Model saved. Transformations in prep_pipe are ignored.")
    else:
        model_ = deepcopy(prep_pipe)
        model_.steps.append(['trained model',model])
    
    import joblib
    model_name = model_name + '.pkl'
    joblib.dump(model_, model_name)
    if verbose:
        print('Transformation Pipeline and Model Succesfully Saved')

    logger.info(str(model_name) + ' saved in current working directory')
    logger.info(str(model_))
    logger.info("save_model() succesfully completed......................................")

def load_model(model_name,
               platform=None,
               authentication=None,
               verbose=True):
    """
    This function loads a previously saved transformation pipeline and model
    from the current active directory into the current python environment.
    Load object must be a pickle file.

    Example
    -------
    >>> saved_lr = load_model('lr_model_23122019')

    This will load the previously saved model in saved_lr variable. The file
    must be in the current directory.

    Parameters
    ----------
    model_name : string, default = none
        Name of pickle file to be passed as a string.

    platform: string, default = None
        Name of platform, if loading model from cloud. Current available options are:
        'aws', 'gcp' and 'azure'.

    authentication : dict
        dictionary of applicable authentication tokens.

        When platform = 'aws':
        {'bucket' : 'Name of Bucket on S3'}

        When platform = 'gcp':
        {'project': 'gcp_pycaret', 'bucket' : 'pycaret-test'}

        When platform = 'azure':
        {'container': 'pycaret-test'}

    verbose: Boolean, default = True
        Success message is not printed when verbose is set to False.

    Returns
    -------
    Model Object

    """

    # ignore warnings
    import warnings
    warnings.filterwarnings('ignore')

    # exception checking
    import sys

    if platform is not None:
        if authentication is None:
            sys.exit("(Value Error): Authentication is missing.")

    if platform is None:

        import joblib
        model_name = model_name + '.pkl'
        if verbose:
            print('Transformation Pipeline and Model Successfully Loaded')
        return joblib.load(model_name)
    # cloud providers
    elif platform == 'aws':
        print('loading model from AWS')

        import boto3
        bucketname = authentication.get('bucket')
        filename = str(model_name) + '.pkl'
        s3 = boto3.resource('s3')
        s3.Bucket(bucketname).download_file(filename, filename)
        filename = str(model_name)
        model = load_model(filename, verbose=False)
        model = load_model(filename, verbose=False)

        if verbose:
            print('Transformation Pipeline and Model Successfully Loaded')

        return model

    elif platform == 'gcp':
        if verbose:
            print('loading model from GCP')
        bucket_name = authentication.get('bucket')
        project_name = authentication.get('project')
        filename = str(model_name) + '.pkl'

        model_downloaded = _download_blob_gcp(project_name,
                                              bucket_name, filename, filename)

        model = load_model(model_name, verbose=False)

        if verbose:
            print('Transformation Pipeline and Model Successfully Loaded')
        return model

    elif platform == 'azure':
        if verbose:
            print('Loading model from Microsoft Azure')

        container_name = authentication.get('container')
        filename = str(model_name) + '.pkl'

        model_downloaded = _download_blob_azure(container_name, filename, filename)

        model = load_model(model_name, verbose=False)

        if verbose:
            print('Transformation Pipeline and Model Successfully Loaded')
        return model
    else:
        print('Platform { } is not supported by pycaret or illegal option'.format(platform))
        # return model

    # import joblib
    # model_name = model_name + '.pkl'
    # if verbose:
    #     print('Transformation Pipeline and Model Sucessfully Loaded')
    #
    # return joblib.load(model_name)

def automl(optimize='R2', use_holdout=False):

    """
    This function returns the best model out of all models created in 
    current active environment based on metric defined in optimize parameter. 

    Parameters
    ----------
    optimize : string, default = 'R2'
        Other values you can pass in optimize param are 'MAE', 'MSE', 'RMSE',
        'RMSLE', and 'MAPE'. 

    use_holdout: bool, default = False
        When set to True, metrics are evaluated on holdout set instead of CV.
    
    """

    import logging

    try:
        hasattr(logger, 'name')
    except:
        logger = logging.getLogger('logs')
        logger.setLevel(logging.DEBUG)
        
        # create console handler and set level to debug
        if logger.hasHandlers():
            logger.handlers.clear()
        
        ch = logging.FileHandler('logs.log')
        ch.setLevel(logging.DEBUG)

        # create formatter
        formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        logger.addHandler(ch)

    logger.info("Initializing automl()")
    logger.info("""automl(optimize={}, use_holdout={})""".\
        format(str(optimize), str(use_holdout)))

    if optimize == 'MAE':
        compare_dimension = 'MAE' 
    elif optimize == 'MSE':
        compare_dimension = 'MSE' 
    elif optimize == 'RMSE':
        compare_dimension = 'RMSE' 
    elif optimize == 'R2':
        compare_dimension = 'R2'
    elif optimize == 'RMSLE':
        compare_dimension = 'RMSLE' 
    elif optimize == 'MAPE':
        compare_dimension = 'MAPE'
        
    scorer = []

    if use_holdout:
        logger.info("Model Selection Basis : Holdout set")
        for i in master_model_container:
            pred_holdout = predict_model(i, verbose=False)
            p = pull()
            display_container.pop(-1)
            p = p[compare_dimension][0]
            scorer.append(p)

    else:
        logger.info("Model Selection Basis : CV Results on Training set")
        for i in create_model_container:
            r = i[compare_dimension][-2:][0]
            scorer.append(r)


    #returning better model
    if compare_dimension == 'R2':
        index_scorer = scorer.index(max(scorer))
    else:
        index_scorer = scorer.index(min(scorer))

    automl_result = master_model_container[index_scorer]

    logger.info("SubProcess finalize_model() called ==================================")
    automl_finalized = finalize_model(automl_result)
    logger.info("SubProcess finalize_model() end ==================================")

    logger.info(str(automl_finalized))
    logger.info("automl() succesfully completed......................................")

    return automl_finalized
    
def pull():
    """
    Returns latest displayed table.

    Returns
    -------
    pandas.DataFrame
        Equivalent to get_config('display_container')[-1]

    """
    return display_container[-1]

def models(type=None):

    """
    Returns table of models available in model library.

    Example
    -------
    >>> all_models = models()

    This will return pandas dataframe with all available 
    models and their metadata.

    Parameters
    ----------
    type : string, default = None
        - linear : filters and only return linear models
        - tree : filters and only return tree based models
        - ensemble : filters and only return ensemble models
      
    Returns
    -------
    pandas.DataFrame
    """

    import pandas as pd

    model_id = ['lr', 'lasso', 'ridge', 'en', 'lar', 'llar', 'omp', 'br', 'ard', 'par', 
                'ransac', 'tr', 'huber', 'kr', 'svm', 'knn', 'dt', 'rf', 'et', 'ada', 
                'gbr', 'mlp', 'xgboost', 'lightgbm', 'catboost']

    model_name = ['Linear Regression',
                   'Lasso Regression',
                   'Ridge Regression',
                   'Elastic Net',
                   'Least Angle Regression',
                   'Lasso Least Angle Regression',
                   'Orthogonal Matching Pursuit',
                   'Bayesian Ridge',
                   'Automatic Relevance Determination',
                   'Passive Aggressive Regressor',
                   'Random Sample Consensus',
                   'TheilSen Regressor',
                   'Huber Regressor',
                   'Kernel Ridge',
                   'Support Vector Machine',
                   'K Neighbors Regressor',
                   'Decision Tree',
                   'Random Forest',
                   'Extra Trees Regressor',
                   'AdaBoost Regressor',
                   'Gradient Boosting Regressor',
                   'Multi Level Perceptron',
                   'Extreme Gradient Boosting',
                   'Light Gradient Boosting Machine',
                   'CatBoost Regressor']

    model_ref = ['sklearn.linear_model.LinearRegression',
                'sklearn.linear_model.Lasso',
                'sklearn.linear_model.Ridge',
                'sklearn.linear_model.ElasticNet',
                'sklearn.linear_model.Lars',
                'sklearn.linear_model.LassoLars',
                'sklearn.linear_model.OMP',
                'sklearn.linear_model.BayesianRidge',
                'sklearn.linear_model.ARDRegression',
                'sklearn.linear_model.PAR',
                'sklearn.linear_model.RANSACRegressor',
                'sklearn.linear_model.TheilSenRegressor',
                'sklearn.linear_model.HuberRegressor',
                'sklearn.kernel_ridge.KernelRidge',
                'sklearn.svm.SVR',
                'sklearn.neighbors.KNeighborsRegressor',
                'sklearn.tree.DecisionTreeRegressor',
                'sklearn.ensemble.RandomForestRegressor',
                'sklearn.ensemble.ExtraTreesRegressor',
                'sklearn.ensemble.AdaBoostRegressor',
                'sklearn.ensemble.GradientBoostingRegressor',
                'sklearn.neural_network.MLPRegressor',
                'xgboost.readthedocs.io',
                'github.com/microsoft/LightGBM',
                'https://catboost.ai']
    
    model_turbo = [True, True, True, True, True, True, True, True, False, True,
                   True, True, True, False, True, True, True, True, True, True,
                   True, False, True, True, True]

    df = pd.DataFrame({'ID' : model_id, 
                       'Name' : model_name,
                       'Reference' : model_ref,
                        'Turbo' : model_turbo})

    df.set_index('ID', inplace=True)

    linear_models = ['lr', 'lasso', 'ridge', 'en', 'lar', 'llar', 'omp', 'br', 'ard', 'par', 'ransac', 'tr', 'huber', 'kr']
    tree_models = ['dt'] 
    ensemble_models = ['rf', 'et', 'gbr', 'xgboost', 'lightgbm', 'catboost', 'ada']

    if type == 'linear':
        df = df[df.index.isin(linear_models)]
    if type == 'tree':
        df = df[df.index.isin(tree_models)]
    if type == 'ensemble':
        df = df[df.index.isin(ensemble_models)]

    return df

def get_logs(experiment_name = None, save = False):

    """
    Returns a table with experiment logs consisting
    run details, parameter, metrics and tags. 

    Example
    -------
    >>> logs = get_logs()

    This will return pandas dataframe.

    Parameters
    ----------
    experiment_name : string, default = None
        When set to None current active run is used.

    save : bool, default = False
        When set to True, csv file is saved in current directory.
      
    Returns
    -------
    pandas.DataFrame
    """
    
    import sys

    if experiment_name is None:
        exp_name_log_ = exp_name_log
    else:
        exp_name_log_ = experiment_name

    import mlflow
    from mlflow.tracking import MlflowClient
    
    client = MlflowClient()

    if client.get_experiment_by_name(exp_name_log_) is None:
        sys.exit('No active run found. Check logging parameter in setup or to get logs for inactive run pass experiment_name.')
    
    exp_id = client.get_experiment_by_name(exp_name_log_).experiment_id    
    runs = mlflow.search_runs(exp_id)

    if save:
        file_name = str(exp_name_log_) + '_logs.csv'
        runs.to_csv(file_name, index=False)

    return runs

def get_config(variable):

    """
    This function is used to access global environment variables.
    Following variables can be accessed:

    - X: Transformed dataset (X)
    - y: Transformed dataset (y)  
    - X_train: Transformed train dataset (X)
    - X_test: Transformed test/holdout dataset (X)
    - y_train: Transformed train dataset (y)
    - y_test: Transformed test/holdout dataset (y)
    - seed: random state set through session_id
    - prep_pipe: Transformation pipeline configured through setup
    - target_inverse_transformer: Target variable inverse transformer
    - folds_shuffle_param: shuffle parameter used in Kfolds
    - n_jobs_param: n_jobs parameter used in model training
    - html_param: html_param configured through setup
    - create_model_container: results grid storage container
    - master_model_container: model storage container
    - display_container: results display container
    - exp_name_log: Name of experiment set through setup
    - logging_param: log_experiment param set through setup
    - log_plots_param: log_plots param set through setup
    - USI: Unique session ID parameter set through setup
    - data_before_preprocess: data before preprocessing
    - target_param: name of target variable
    - gpu_param: use_gpu param configured through setup

    Example
    --------
    >>> X_train = get_config('X_train') 

    This will return X_train transformed dataset.
        
    Returns
    -------
    variable
    """

    import logging

    try:
        hasattr(logger, 'name')
    except:
        logger = logging.getLogger('logs')
        logger.setLevel(logging.DEBUG)
        
        # create console handler and set level to debug
        if logger.hasHandlers():
            logger.handlers.clear()
        
        ch = logging.FileHandler('logs.log')
        ch.setLevel(logging.DEBUG)

        # create formatter
        formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        logger.addHandler(ch)

    logger.info("Initializing get_config()")
    logger.info("""get_config(variable={})""".\
        format(str(variable)))

    if variable == 'X':
        global_var = X
    
    if variable == 'y':
        global_var = y

    if variable == 'X_train':
        global_var = X_train

    if variable == 'X_test':
        global_var = X_test

    if variable == 'y_train':
        global_var = y_train

    if variable == 'y_test':
        global_var = y_test

    if variable == 'seed':
        global_var = seed

    if variable == 'prep_pipe':
        global_var = prep_pipe

    if variable == 'target_inverse_transformer':
        global_var = target_inverse_transformer

    if variable == 'folds_shuffle_param':
        global_var = folds_shuffle_param
        
    if variable == 'n_jobs_param':
        global_var = n_jobs_param

    if variable == 'html_param':
        global_var = html_param

    if variable == 'create_model_container':
        global_var = create_model_container

    if variable == 'master_model_container':
        global_var = master_model_container

    if variable == 'display_container':
        global_var = display_container

    if variable == 'exp_name_log':
        global_var = exp_name_log

    if variable == 'logging_param':
        global_var = logging_param

    if variable == 'log_plots_param':
        global_var = log_plots_param

    if variable == 'USI':
        global_var = USI

    if variable == 'data_before_preprocess':
        global_var = data_before_preprocess

    if variable == 'target_param':
        global_var = target_param

    if variable == 'gpu_param':
        global_var = gpu_param

    logger.info("Global variable: " + str(variable) + ' returned')
    logger.info("get_config() succesfully completed......................................")

    return global_var

def set_config(variable,value):

    """
    This function is used to reset global environment variables.
    Following variables can be accessed:

    - X: Transformed dataset (X)
    - y: Transformed dataset (y)  
    - X_train: Transformed train dataset (X)
    - X_test: Transformed test/holdout dataset (X)
    - y_train: Transformed train dataset (y)
    - y_test: Transformed test/holdout dataset (y)
    - seed: random state set through session_id
    - prep_pipe: Transformation pipeline configured through setup
    - target_inverse_transformer: Target variable inverse transformer
    - folds_shuffle_param: shuffle parameter used in Kfolds
    - n_jobs_param: n_jobs parameter used in model training
    - html_param: html_param configured through setup
    - create_model_container: results grid storage container
    - master_model_container: model storage container
    - display_container: results display container
    - exp_name_log: Name of experiment set through setup
    - logging_param: log_experiment param set through setup
    - log_plots_param: log_plots param set through setup
    - USI: Unique session ID parameter set through setup
    - data_before_preprocess: data before preprocessing
    - target_param: name of target variable
    - gpu_param: use_gpu param configured through setup

    Example
    --------
    >>> set_config('seed', 123) 

    This will set the global seed to '123'.
        
      
    """

    import logging

    try:
        hasattr(logger, 'name')
    except:
        logger = logging.getLogger('logs')
        logger.setLevel(logging.DEBUG)
        
        # create console handler and set level to debug
        if logger.hasHandlers():
            logger.handlers.clear()
        
        ch = logging.FileHandler('logs.log')
        ch.setLevel(logging.DEBUG)

        # create formatter
        formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        logger.addHandler(ch)

    logger.info("Initializing set_config()")
    logger.info("""set_config(variable={}, value={})""".\
        format(str(variable), str(value)))

    if variable == 'X':
        global X
        X = value

    if variable == 'y':
        global y
        y = value

    if variable == 'X_train':
        global X_train
        X_train = value

    if variable == 'X_test':
        global X_test
        X_test = value

    if variable == 'y_train':
        global y_train
        y_train = value

    if variable == 'y_test':
        global y_test
        y_test = value

    if variable == 'seed':
        global seed
        seed = value

    if variable == 'prep_pipe':
        global prep_pipe
        prep_pipe = value

    if variable == 'target_inverse_transformer':
        global target_inverse_transformer
        target_inverse_transformer = value

    if variable == 'folds_shuffle_param':
        global folds_shuffle_param
        folds_shuffle_param = value

    if variable == 'n_jobs_param':
        global n_jobs_param
        n_jobs_param = value

    if variable == 'html_param':
        global html_param
        html_param = value

    if variable == 'create_model_container':
        global create_model_container
        create_model_container = value

    if variable == 'master_model_container':
        global master_model_container
        master_model_container = value

    if variable == 'display_container':
        global display_container
        display_container = value

    if variable == 'exp_name_log':
        global exp_name_log
        exp_name_log = value

    if variable == 'logging_param':
        global logging_param
        logging_param = value

    if variable == 'log_plots_param':
        global log_plots_param
        log_plots_param = value

    if variable == 'USI':
        global USI
        USI = value

    if variable == 'data_before_preprocess':
        global data_before_preprocess
        data_before_preprocess = value

    if variable == 'target_param':
        global target_param
        target_param = value

    if variable == 'gpu_param':
        global gpu_param
        gpu_param = value

    logger.info("Global variable:  " + str(variable) + ' updated')
    logger.info("set_config() succesfully completed......................................")

def get_system_logs():

    """
    Read and print 'logs.log' file from current active directory.
    """

    file = open('logs.log', 'r')
    lines = file.read().splitlines()
    file.close()

    for line in lines:
        if not line:
            continue

        columns = [col.strip() for col in line.split(':') if col]
        print(columns)

def _create_bucket_gcp(project_name, bucket_name):
    """
    Creates a bucket on Google Cloud Platform if it does not exists already

    Example
    -------
    >>> _create_bucket_gcp(project_name='GCP-Essentials', bucket_name='test-pycaret-gcp')

    Parameters
    ----------
    project_name : string
        A Project name on GCP Platform (Must have been created from console).

    bucket_name : string
        Name of the storage bucket to be created if does not exists already.

    Returns
    -------
    None
    """

    # bucket_name = "your-new-bucket-name"
    from google.cloud import storage
    storage_client = storage.Client(project_name)

    buckets = storage_client.list_buckets()

    if bucket_name not in buckets:
        bucket = storage_client.create_bucket(bucket_name)
        logger.info("Bucket {} created".format(bucket.name))
    else:
        raise FileExistsError('{} already exists'.format(bucket_name))

def _upload_blob_gcp(project_name, bucket_name, source_file_name, destination_blob_name):

    """
    Upload blob to GCP storage bucket

    Example
    -------
    >>> _upload_blob_gcp(project_name='GCP-Essentials', bucket_name='test-pycaret-gcp', \
                        source_file_name='model-101.pkl', destination_blob_name='model-101.pkl')

    Parameters
    ----------
    project_name : string
        A Project name on GCP Platform (Must have been created from console).

    bucket_name : string
        Name of the storage bucket to be created if does not exists already.

    source_file_name : string
        A blob/file name to copy to GCP

    destination_blob_name : string
        Name of the destination file to be stored on GCP

    Returns
    -------
    None
    """

    # bucket_name = "your-bucket-name"
    # source_file_name = "local/path/to/file"
    # destination_blob_name = "storage-object-name"
    from google.cloud import storage
    storage_client = storage.Client(project_name)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    logger.info(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )

def _download_blob_gcp(project_name, bucket_name, source_blob_name, destination_file_name):
    """
    Download a blob from GCP storage bucket

    Example
    -------
    >>> _download_blob_gcp(project_name='GCP-Essentials', bucket_name='test-pycaret-gcp', \
                          source_blob_name='model-101.pkl', destination_file_name='model-101.pkl')

    Parameters
    ----------
    project_name : string
        A Project name on GCP Platform (Must have been created from console).

    bucket_name : string
        Name of the storage bucket to be created if does not exists already.

    source_blob_name : string
        A blob/file name to download from GCP bucket

    destination_file_name : string
        Name of the destination file to be stored locally

    Returns
    -------
    Model Object
    """

    # bucket_name = "your-bucket-name"
    # source_blob_name = "storage-object-name"
    # destination_file_name = "local/path/to/file"
    from google.cloud import storage
    storage_client = storage.Client(project_name)

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    if destination_file_name is not None:
        blob.download_to_filename(destination_file_name)

        logger.info(
            "Blob {} downloaded to {}.".format(
                source_blob_name, destination_file_name
            )
        )

    return blob

def _create_container_azure(container_name):
    """
    Creates a storage container on Azure Platform. gets the connection string from the environment variables.

    Example
    -------
    >>>  container_client = _create_container_azure(container_name='test-pycaret-azure')

    Parameters
    ----------
    container_name : string
        Name of the storage container to be created if does not exists already.

    Returns
    -------
    cotainer_client
    """

    # Create the container
    import os, uuid
    from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
    connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    container_client = blob_service_client.create_container(container_name)
    logger.info('{} has been created successfully on Azure platform')
    return container_client

def _upload_blob_azure(container_name, source_file_name, destination_blob_name):
    """
    Upload blob to Azure storage  container

    Example
    -------
    >>>  _upload_blob_azure(container_name='test-pycaret-azure', source_file_name='model-101.pkl', \
                           destination_blob_name='model-101.pkl')

    Parameters
    ----------
    container_name : string
        Name of the storage bucket to be created if does not exists already.

    source_file_name : string
        A blob/file name to copy to Azure

    destination_blob_name : string
        Name of the destination file to be stored on Azure

    Returns
    -------
    None
    """

    import os, uuid
    from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
    connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')

    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    # Create a blob client using the local file name as the name for the blob
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=destination_blob_name)

    logger.info("\nUploading to Azure Storage as blob:\n\t" + source_file_name)

    # Upload the created file
    with open(source_file_name, "rb") as data:
      blob_client.upload_blob(data)

def _download_blob_azure(container_name, source_blob_name, destination_file_name):
    """
    Download blob from Azure storage  container

    Example
    -------
    >>>  _download_blob_azure(container_name='test-pycaret-azure', source_blob_name='model-101.pkl', \
                             destination_file_name='model-101.pkl')

    Parameters
    ----------
    container_name : string
        Name of the storage bucket to be created if does not exists already.

    source_blob_name : string
        A blob/file name to download from Azure storage container

    destination_file_name : string
        Name of the destination file to be stored locally

    Returns
    -------
    None
    """

    import os, uuid
    from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
    print("\nDownloading blob to \n\t" + destination_file_name)

    connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    # Create a blob client using the local file name as the name for the blob
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=source_blob_name)

    if destination_file_name is not None:
        with open(destination_file_name, "wb") as download_file:
          download_file.write(blob_client.download_blob().readall())

        logger.info(
            "Blob {} downloaded to {}.".format(
                source_blob_name, destination_file_name
            )
        )