import numpy as np
import pandas as pd

log_file = r'C:\Users\Tagami\OneDrive\Documents\GitHub\ai_art_classification_model\mobilenetv2_log.txt'
model = 'MobileNetV2'
file = open(log_file, 'r') # The 'r' allows us to read it
file_data = file.readlines()
file_data = ''.join(file_data)
print(file_data)

def paritition_epoch(file_data):
    log_data = []
    x = 0
    after = file_data
    while x < 1:
        before, keyword, after = after.partition('Epoch ')
        before, keyword, after = after.partition('/')
        c_epoch = float(before)
        print('Epoch', c_epoch)
        before, keyword, after = after.partition('[')
        before, keyword, after = after.partition(':')
        c_tr_dur = float(before) * 60
        before, keyword, after = after.partition('<')
        c_tr_dur = float(before) + c_tr_dur
        print('Dur: ', c_tr_dur)
        before, keyword, after = after.partition(',  ')
        before, keyword, after = after.partition('it/s')
        c_tr_its = float(before)
        print('train it/s: ', c_tr_its)
        before, keyword, after = after.partition('train Loss: ')
        before, keyword, after = after.partition(' Accuracy: ')
        c_tr_loss = float(before)
        print('train loss: ', c_tr_loss)
        before, keyword, after = after.partition('\n')
        c_tr_acc = float(before)
        print('train Acc: ', c_tr_acc)
        before, keyword, after = after.partition('[')
        before, keyword, after = after.partition(':')
        c_te_dur = float(before) * 60
        before, keyword, after = after.partition('<')
        c_te_dur = float(before) + c_te_dur
        print('test Dur: ', c_te_dur)
        before, keyword, after = after.partition(',  ')
        before, keyword, after = after.partition('it/s')
        c_te_its = float(before)
        print('test it/s: ', c_te_its)
        before, keyword, after = after.partition('test Loss: ')
        before, keyword, after = after.partition(' Accuracy: ')
        c_te_loss = float(before)
        print('test loss: ', c_te_loss)
        before, keyword, after = after.partition('\n')
        c_te_acc = float(before)
        print('test Acc: ', c_te_acc)
        c_log_data = [c_epoch, c_tr_dur, c_tr_its, c_tr_loss, c_tr_acc, c_te_dur, c_te_its, c_te_loss, c_te_acc]
        log_data.append(c_log_data)
        before_try, keyword_try, after_try = after.partition('Epoch ')
        if after_try == '':
            print('Fully scanned all epochs')
            before, keyword, after = after.partition('in ')
            before, keyword, after = after.partition('m ')
            comp = float(before) * 60
            before, keyword, after = after.partition('s')
            comp = float(before) + comp
            before, keyword, after = after.partition(': ')
            best_acc = float(after)
            break
    return log_data

def write_to_csv(log_data, model):
    arr = np.asarray(log_data)
    pd.DataFrame(arr).to_csv(f'{model}_log.csv',header = ['Epoch', 'Train Duration', 'Train it/s', 'Train loss', 'Train accuracy', 'Test Duration', 'Test it/s', 'Test loss', 'Test accuracy'], index=None)  
    
log_data = paritition_epoch(file_data)    
print(log_data)
write_to_csv(log_data, model)
    
