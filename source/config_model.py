# -*- coding: utf-8 -*-

import copy

##############################################################################################   
def y_norm(y, inverse=True, mode='boxcox'):
    ## Normalize the input/output
    if mode == 'boxcox':
        width0 = 53.0  # 0,1 factor
        k1 = 0.6145279599674994  # Optimal boxCox lambda for y
        if inverse:
            y2 = y * width0
            y2 = ((y2 * k1) + 1) ** (1 / k1)
            return y2
        else:
            y1 = (y ** k1 - 1) / k1
            y1 = y1 / width0
            return y1

    if mode == 'norm':
        m0, width0 = 0.0, 350.0  ## Min, Max
        if inverse:
            y1 = (y * width0 + m0)
            return y1

        else:
            y2 = (y - m0) / width0
            return y2
    else:
        return y

##############################################################################################  
##############################################################################################  
"""
       ##  'models.model_bayesian_pyro'   'model_widedeep'
       
        ### Al SKLEARN API
        #['ElasticNet', 'ElasticNetCV', 'LGBMRegressor', 'LGBMModel', 'TweedieRegressor', 'Ridge']:
       mod    = 'models.model_sklearn'


# cols['cols_model'] = cols["colnum_onehot"] + cols["colcat_onehot"] + cols["colcross_onehot"]


"""
        

##############################################################################################  
def elasticnetcv(path_model_out):
    def post_process_fun(y):
        return y_norm(y, inverse=True, mode='boxcox')

    def pre_process_fun(y):
        return y_norm(y, inverse=False, mode='boxcox')

    model_dict = {'model_pars': {'model_name': 'ElasticNetCV'
        , 'model_path': path_model_out
        , 'model_pars': {}  # default ones
        , 'post_process_fun': post_process_fun 
        , 'pre_process_pars': {'y_norm_fun' : pre_process_fun,
                               }
                                 },
      'compute_pars': { 'metric_list': ['root_mean_squared_error', 'mean_absolute_error',
                                        'explained_variance_score',  'r2_score', 'median_absolute_error']
                      },
      'data_pars': {
          'cols_model_group': [ 'colnum_onehot', 'colcat_onehot', 'colcross_onehot' ]    
         ,'cols_model': []  # cols['colcat_model'],
         ,'coly': []        # cols['coly']
         ,'filter_pars': { 'ymax' : 100000.0 ,'ymin' : 0.0 }   ### Filter data
                  }}
    return model_dict               



def lightgbm(path_model_out) :
    """
      Huber Loss includes L1  regurarlization         
      We test different features combinaison, default params is optimal
    """
    def post_process_fun(y):
        return y_norm(y, inverse=True, mode='boxcox')

    def pre_process_fun(y):
        return y_norm(y, inverse=False, mode='boxcox')

    model_dict = {'model_pars': {'model_name': 'LGBMRegressor'
        , 'model_path': path_model_out
        , 'model_pars': {'objective': 'huber', }  # default
        , 'post_process_fun': post_process_fun
        , 'pre_process_pars': {'y_norm_fun' :  copy.deepcopy(pre_process_fun) ,
                               }
                                 },
      'compute_pars': { 'metric_list': ['root_mean_squared_error', 'mean_absolute_error',
                                        'explained_variance_score', 'r2_score', 'median_absolute_error']
                      },
    
      'data_pars': {
          # cols['cols_model'] = cols["colnum"] + cols["colcat_bin"]  # + cols[ "colcross_onehot"]
          'cols_model_group': [ 'colnum', 'colcat_bin']    
         ,'cols_model': []  # cols['colcat_model'],
         ,'coly': []        # cols['coly']
         ,'filter_pars': { 'ymax' : 100000.0 ,'ymin' : 0.0 }   ### Filter data
         
         }}
    return model_dict               


def bayesian_pyro(path_model_out) :
    def post_process_fun(y):
        return y_norm(y, inverse=True, mode='boxcox')

    def pre_process_fun(y):
        return y_norm(y, inverse=False, mode='boxcox')

    model_dict = {'model_pars': {'model_name': 'model_bayesian_pyro'
        , 'model_path': path_model_out
        , 'model_pars': {'input_width': 112, }  # default
        , 'post_process_fun': post_process_fun
        
                                 },
      'compute_pars': {'compute_pars': {'n_iter': 1200, 'learning_rate': 0.01}
          , 'metric_list': ['root_mean_squared_error', 'mean_absolute_error',
                            'explained_variance_score', 'r2_score', 'median_absolute_error']
          , 'max_size': 1000000
          , 'num_samples': 300
        , 'pre_process_pars': {'y_norm_fun' : pre_process_fun,
                               }        

                                   },
      'data_pars': {
          'cols_model_group': [ 'colnum_onehot', 'colcat_onehot' ]    
         ,'cols_model': []  # cols['colcat_model'],
         ,'coly': []        # cols['coly']
         ,'filter_pars': { 'ymax' : 100000.0 ,'ymin' : 0.0 }   ### Filter data
                  }}
    return model_dict               
                
                  

def glm() :
    def post_process_fun(y):
        return y_norm(y, inverse=True, mode='norm')

    def pre_process_fun(y):
        return y_norm(y, inverse=False, mode='norm')


    cols['cols_model'] = cols["colnum_onehot"] + cols["colcat_onehot"]  # cols[ "colcross_onehot"]
    model_dict = {'model_pars': {'model_name': 'TweedieRegressor'  # Ridge
        , 'model_path': path_model_out
        , 'model_pars': {'power': 0, 'link': 'identity'}  # default ones
        , 'pre_process_pars': {'y_norm_fun' : pre_process_fun }
                                 },
                  'compute_pars': {'metric_list': ['root_mean_squared_error', 'mean_absolute_error',
                                                   'explained_variance_score',  'r2_score', 'median_absolute_error']
                                  },
                  'data_pars': {
                      'cols_model': cols['cols_model'],
                      'coly': cols['coly']
                  }}
    return model_dict               
               
                  
 
    
