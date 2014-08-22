from gala import imio, classify, features, agglo, evaluate as ev


gt_train, pr_train, ws_train = (map(imio.read_h5_stack,
                                    ['train-gt.lzf.h5', 'train-p1.lzf.h5',
                                     'train-ws.lzf.h5']))