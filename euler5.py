#Euler法による常微分方程式の解法プログラム
import matplotlib
import numpy as np  #NumPyライブラリ
import matplotlib.pyplot as plt  #データ可視化ライブラリ

#以前のビーム照射による積分効果をビーム強度ごとに取り入れる
#P0もプロットされるようにした

#導関数dy/dt
def func_dydt(t, y, TD,TL,Pe,alpha,beta,I,t0,S):
   # print(S)

    return (Pe-y)/TD-(1/TL + alpha*0.00001*(I*t+S) + beta*0.00001*I)*y  #dy/dt = 
   # return (Pe-y)/TD-(1/TL + alpha*I*(t+16102/3600) + beta*I)*y  #dy/dt = 



#Euler法（導関数、tの初期値、yの初期値、刻み幅dt）
def euler(func_dydt, TD,TL,Pe,alpha,beta,I,t0 ,t, y, S,dt=1e-3):
    #print("I={:.7f},S={:.7f}".format(I, S))
    if t > 2650./60: 
        S = I * (3480/60 - 2180/60)
        I = 0. 
    dy = func_dydt(t, y, TD,TL,Pe,alpha,beta,I,t0,S)*dt  #変化量を計算

    t += dt  #変数を更新
    y += dy  #変化量を加えて更新

    return t, y


#常微分方程式を逐次計算（導関数、yの初期値、tの開始点、tの終了点、刻み幅dt）
def ode_calc(func_dydt,TD,TL,Pe,alpha,beta,I,t0, P0, t_start, t_end,day,S, dt=1/60):
    num_calc = 0  #計算回数
    t_div = np.abs((t_end-t_start)/dt)  #格子分割数
    if(t_end<t_start):  #負の方向に計算する時は刻み幅の符号を反転
        dt = -dt

    #初期値
    t = t_start  #独立変数t
    y = P0  #従属変数y
    print("t = {:.7f},  y = {:.7f}".format(t, y))

    #グラフ用データを追加
    t_list = [t]
    y_list = [y]


    #ずっと繰り返す
    while(True):
        with open('/Users/matsuitakaya/Desktop/研究室/偏極陽子/作業/標的系/グラフ/pol_HIMAC/本測定/int_100/radiationloss/test.txt'.format(day,P0,alpha,beta), mode='a') as f:
           # f.write("{:.7f},  {:.7f}\n".format(t*60, y))
            if (len(t_list)-1)%20 == 0:
                    #print("asd")
                    #時間をminに直してファイルに書き込む
                f.write("{:.7f}  {:.7f}\n".format(t*60, y))
        t, y = euler(func_dydt,TD,TL,Pe,alpha,beta,I,t0, t, y, S, dt)

        #print("t = {:.7f},  y = {:.7f}".format(t, y))
        #print("{:.7f},  {:.7f}".format(t, y))
        
        
        

            #実験データと合わせるために20分ごとにデータをファイルに書き込む
            #ここで生成するファイルは単位が[h]なので20min=0.3333...h→33行目
            
            
            
            
    #f.write("{:.7f},  {:.7f}\n".format(t, y))
       

        

    #グラフ用データを追加
        t_list.append(t)
        y_list.append(y)

        num_calc += 1  #計算回数を数える

        #「計算回数が格子分割数以上」ならば終了
        if(t_div<=num_calc):
        #if(t>480.):
            print("Finished.")
            print()
            break

    return t_list, y_list


#可視化
def visualization(t_list, y_list):
    plt.xlabel("$t$")  #x軸の名前
    plt.ylabel("$y(t)$")  #y軸の名前
    plt.grid()  #点線の目盛りを表示

    plt.plot(t_list,y_list, label="$y(t)$", color='#ff0000')  #折線グラフで表示
    plt.legend(loc='best') #凡例(グラフラベル)を表示
    plt.show()  #グラフを表示


#メイン実行部
def main1(TD,TL,Pe,alpha,beta,I,t0,day,P0,S):
   # if (__name__ == '__main__'):
        #Euler法でdt離れた点の値を取得
    f = open('/Users/matsuitakaya/Desktop/研究室/偏極陽子/作業/標的系/グラフ/pol_HIMAC/本測定/int_100/radiationloss/test.txt'.format(day,P0,alpha,beta), 'w')
    #f.write("{:.7f},  {:.7f}\n".format( t0, P0))
    t, y = euler(func_dydt, TD,TL,Pe,alpha,beta,I,t0 ,0.0, 0.0,S)
    f = open('/Users/matsuitakaya/Desktop/研究室/偏極陽子/作業/標的系/グラフ/pol_HIMAC/本測定/int_100/radiationloss/test.txt'.format(day,P0,alpha,beta), 'w')
    #f = open("test.txt",'w')
    #print("t = {:.7f},  y = {:.7f}".format(t, y))
   # print("{:.7f},  {:.7f}".format(t, y))


    #常微分方程式を逐次計算（導関数、TD,TL,Pe,alpha,beta,I,t0,yの初期値、tの開始点、tの終了点、(刻み幅dt）,日付(ファイル名))
    t_list, y_list = ode_calc(func_dydt,TD,TL,Pe,alpha,beta,I,t0, P0, 2180/60,3480/60, day,S)
    f.close()
    #print(111)
    #結果を可視化
    #visualization(t_list, y_list)
    
    #実験データも一緒にプロットしたい
    #visualization(2180t_list, 2180y_list)

if (__name__ == '__main1__'):
    main1()