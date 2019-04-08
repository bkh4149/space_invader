# coding: utf-8
import sys
import math
import random
import time
import sys 
import pygame 
from pygame.locals import *

pygame.init()



#global
sc = pygame.display.set_mode(( 800, 600)) 

#得点表示用
msgothic = r'c:\windows\fonts\msgothic.ttc'
mf = pygame.font.Font(msgothic, 24)
mf2 = pygame.font.Font(msgothic, 48)

#アイコン
giv1 = pygame.image.load("invader1.png").convert_alpha()#インベーダー　　50x50
giv2 = pygame.image.load("invader2.png").convert_alpha()#インベーダー２　50x50
gply = pygame.image.load("player.png").convert_alpha()#砲台　　　　　　　50x50
gagm = pygame.image.load("age.png").convert_alpha()#agmミサイル　　　　　20x50
gsgm = pygame.image.load("oti.png").convert_alpha()#sgmミサイル　　　　　20x50

gsh1 = pygame.image.load("sh_blk.png").convert_alpha()#シェルター　　　　20x20
gsh2 = pygame.image.load("sh_blk2.png").convert_alpha()#残骸
gsh3 = pygame.image.load("sh_blk3.png").convert_alpha()#残骸
gsh4 = pygame.image.load("sh_blk4.png").convert_alpha()#残骸


#アイコンの幅と高さ
iw=giv1.get_width()
ih=giv1.get_height()
iw2=gagm.get_width()

#インベーダー行列
tb_inv = [[1 for i in range(8)] for j in range(4)]

#シェルター行列
tb_sh =[[[1 for i in range(5)] for j in range(3)] for k in range(4)]


#インベーダー描画　（インベーダー行列tb_inv　にしたがって1なら描画
def invader(sc,state,xinv,yinv,xagm,yagm,fhit,left_inv):
  for y in range (4):#横5行
    for x in range (8):#縦8個
      #import pdb;pdb.set_trace() #debug

      #行列中、x,yのインベーダが生きているなら以下実行
      if tb_inv[y][x]==1:#生きている

        #インベーダの座標
        ix=xinv+x*70
        iy=yinv+y*60
        
        #あげミサイルとの衝突判定
        rx=xagm-ix
        #zx=iw/4+iw2/4
        if -25<rx and rx<50: #x当たり
            ry=math.fabs(yagm-iy)
            zy=ih
            if ry<zy: #当たり
                tb_inv[y][x]=0
                left_inv-=1
                fhit=1
        #インヴェーダの描画（メモリ書き込み）
        if state==1:
            sc.blit(giv1, Rect(ix,iy,iw,ih))

        else:
            sc.blit(giv2, Rect(ix,iy,iw,ih))

        #end(if state==1:
      #--end (if tb_inv[x,y]==1:
    #end (for x in range (0,8):
  #end(for y in range (0,4):
  return fhit,left_inv


#プレイヤー描画
def player(sc,xply,yply):
    sc.blit(gply ,Rect(xply,yply,iw,ih))

#上げミサイル描画　当たり判定
def agm(sc,xagm,yagm):
    sc.blit(gagm ,Rect(xagm,yagm,iw2,ih))
    fh_agm_shl=0

    #シェルターと当たっているかチェック
    for tk in range (4):
        dx=xagm-(120+tk*150)
        if -10 < dx and dx < 90: #x当たり
            dy=350-yagm
            if -40 < dy and dy<30: #y当たり
                ix=int((dx+10)/20)
                iy=int(dy/20)

                #print (tk)
                #print(dx,ix,dy,iy) 
                #import pdb;pdb.set_trace() #debug
                if tb_sh[tk][iy][ix] ==1: #真のあたり
 
                    tb_sh[tk][iy][ix] =0
                    fh_agm_shl=1


    return fh_agm_shl

#シェルター描画　４つ分
#shelter　当たり判定
def shelter(sc):

    #import pdb;pdb.set_trace() #debug
    for tk in range(4): #0,1,2,3
      for ty in range(3): #0,1,2
        for tx in range(5): #0,1,2,3,4
           ttx=120+tk*150
           tty=350

           #tr=random.randint(0,10)
           if tb_sh[tk][ty][tx]==1:
               #シェルター描画　レンガ１つ分
               sc.blit(gsh1 ,Rect(ttx+tx*20,tty+ty*20,20,20))

           else:#残骸　or　何も書かない
               if ty==0:
                   if tb_sh[tk][1][tx]==0:
                       pass
                   else:
                       sc.blit(gsh3 ,Rect(ttx+tx*20,tty+ty*20,20,20))
               elif ty==1:
                   if tb_sh[tk][2][tx]==0:
                       pass
                   else:
                       sc.blit(gsh2 ,Rect(ttx+tx*20,tty+ty*20,20,20))
               else:#ty=2
                   if tb_sh[tk][1][tx]==0:
                       pass
                   else:
                       sc.blit(gsh4 ,Rect(ttx+tx*20,tty+ty*20,20,20))



#sgmミサイル描画　当たり判定
#　砲台やシェルターとの当たり判定
#def sgm(sc,xsgm,ysgm,xply,yply,xshl,yshl):
def sgm(sc,xsgm,ysgm,xply,yply):
    fh_sgm_ply=0
    fh_sgm_shl=0
    sc.blit(gsgm ,Rect(xsgm,ysgm,5,ih))


    #シェルターと当たっているかチェック
    for tk in range (4):
        dx=xsgm-(120+tk*150)
        if -10 < dx and dx < 90: #x当たり
            dy=350-ysgm
            if -40 < dy and dy<30: #y当たり
                ix=int((dx+10)/20)
                iy=int((dy-10)/20)

                #print (tk)
                #print(dx,ix,dy,iy) 
                #import pdb;pdb.set_trace() #debug
                if tb_sh[tk][iy][ix] ==1: #真のあたり
 
                    tb_sh[tk][iy][ix] =0
                    fh_sgm_shl=1


    #砲台と当たっているかチェック
    tx=xsgm-xply
    if -2 < tx and tx <34: #x当たり
        ty=math.fabs(ysgm-yply)
        if ty<20: #当たり
           fh_sgm_ply=1

    return fh_sgm_ply,fh_sgm_shl

def lenchk():
#インベーダの全体の長さの計測　
    xl_inv=70*8
    sum=[0]*8

    for tx in range(8):
        for ty in range(4):
            sum[tx] +=tb_inv[ty][tx]

    #ここからは最小値、最大値を求める問題
    #左端から最初に0以外が来るまで
    min=0
    for tx in range(8):
        if sum[tx]>0:
            min=tx
            break

    #右端から最初に0以外が来るまで
    max=7
    for tx in reversed(range(8)):
        if sum[tx]>0:
            max=tx
            #import pdb;pdb.set_trace() #debug
            break

    return min,max

def main():
#    pygame.display.set_caption("taxi game")

    ck = pygame.time.Clock()

    left_ply=3
    left_inv=32
    #インヴェーダの位置
    xinv=102
    yinv=50
    #インヴェーダの速度
    vinv=2
    fclear=0 #インベーダーを全部やっつけたか

    xrlim=700   #折り返す右端
    xllim=100   #

    while True:#砲台1つ分

        #コミュニケーションflag
        fspky=0 #space key
        fh=0 	#agmミサイルがインベーダにhitか
        fh2=0 	#sgm ミサイルが砲台にhitか　　

        ct=0	#カウンタ　10になるごとにインベーダを動かす
        state=0 #インベーダーの手の上げ下げ

        #砲台（プレイヤー）の位置
        xply=400
        vply=0
        yply=450
    
        #あげミサイルの位置、状態
        xagm=xply
        yagm=yply
        fagm=0    #0:未発射  1:発射後　上昇中


        #sgmミサイルのフラグ、位置、状態、総個数
        sum_sgm=5
        fsgm=[0]*sum_sgm
        xsgm=[0]*sum_sgm
        ysgm=[0]*sum_sgm
    
        fct=10
  

        while True:#1画面分　1フレーム
    
            start = time.time() #1フレームの時間測定　16msec以内ならOK

            #画面クリア
            sc.fill(( 255, 255, 255))
            #pygame. draw.rect(sc,(255, 0, 255),Rect(xllim,100,xrlim-xllim,300)) 
    


            #砲台残り表示
            mm="砲台="+str(left_ply)+"  invader "+str(left_inv)
            tm = mf.render(mm, False,(0,0,0))
            sc.blit(tm,(200,10)) 


            #インベーダー スピード調節　後半早くする
            #　　最後の一匹　激速
            ct+=1
            if left_inv <10:
                fct=5

                #　　最後の一匹　激速
                if left_inv ==1:
                   fct=1
                   if vinv>0:
                       vinv = 10
                   else:
                       vinv= -10

            if ct>fct:#内部クロック10フレームに一回、全体を動かす
                ct=0
                xinv += vinv

                min,max=lenchk() #全体長チェック

                if xinv+max*70>xrlim-60:#画面の右端de折り返す
                    #import pdb;pdb.set_trace() #debug
                    vinv *=-1
                    yinv +=10
                    
                elif xinv+min*70 <xllim:#画面の左端なら右に折り返す
                    #import pdb;pdb.set_trace() #debug
                    vinv *=-1
                    yinv +=10

                #end (if else
    
                state +=1
                if state==2:#手を上げたり下げたりアニメのためのフラグ
                    state=0
    
            #インベーダーの描画　動かすのは10カウントに1回だが描画は毎回やる
            #　そうしないと消えた感じがする
            #　大量の引数と戻り値を持つので整理
            #　　def invader(sc,state,xinv,yinv,xagm,yagm,fh):
            #    return fhit
            fh,left_inv=invader(sc,state,xinv,yinv,xagm,yagm,fh,left_inv)
    
            #インベーダーが上げミサイルに当たっているならキーフラグリセット
            if fh==1:
               fspky=0
               fagm=0
               #インベーダーが全滅ならブレーク
               if left_inv==0:
                   break


            #下げミサイル
            #下げミサイル発生
            rr=random.random()
            if rr<0.7:
                rx=random.randint(0,7)
                ry=random.randint(0,3)
                #ソノ位置のインベーダーが生きているなら
                if tb_inv[ry][rx]==1:
                    #さげミサイル行列fsgmの空いているところに登録
                    #さげミサイル行列が最初にゼロのところを探し、書き込んでいく
                    for iss in range(sum_sgm):
                        #import pdb;pdb.set_trace() #debug
                        #10以上は無視
                        if fsgm[iss]==0:
                            fsgm[iss]=1
                            xsgm[iss]=xinv+rx*70+20
                            ysgm[iss]=yinv+ry*60+20
                            break #処理が終わったらすぐにforを抜ける
                            #ここでbreakをいれないと10個全部に書き込んでしまう
                     #end for    　
                #end if
            #end if  

            #sgmミサイル def sgm(sc,xsgm,ysgm):

            fh3=0
            for ss in range(sum_sgm):
                #さげミサイル行列が1なら描画
                if fsgm[ss]==1:
                   #def sgm(sc,xsgm,ysgm,xply,yply):
                   #　下げミサイルの描画時に砲台との当たり判定をやっている
                   #　戻り値fh2は下げミサイルが砲台に当たったか、１なら当たり
                   #　戻り値fh4は下げミサイルがシェルターに当たったか、
                   fh2,fh4=sgm(sc,xsgm[ss],ysgm[ss],xply,yply)

                   fh3 += fh2

                   #下げミサイル位置更新
                   ysgm[ss] += 10

                   #下げミサイルの位置が450以上なら行列から削除
                   if ysgm[ss]> 450:
                      fsgm[ss]=0

                   #下げミサイルがシェルタに当っていれば行列から削除
                   if fh4==1:
                      #import pdb;pdb.set_trace() #debug
                      fsgm[ss]=0

            #end(下げミサイル

            #shelter
            shelter(sc)


            #player(sc)砲台#
            # 砲台が下げミサイルに当たっていたら
            if fh3 > 0:
                left_ply -=1
                break #（while　1フレーム分）抜け

            elif fh3==0:#当たっていなければ以下(砲台を動かす)
                xply += vply
                if xply>650:
                    xply=650
                elif xply <10:
                    xply=10
                player(sc,xply,yply)
            
                #あげミサイル#
                #砲台が下げミサイルにヒットしておらず、fh=0
                #　かつキーボードからスペースが押され　fspky=1　
                #　かつ上げミサイルが未発射　fagm==0　なら
                if fh==0 and fspky==1 and fagm==0:
                    #上げミサイル初期設定
                    fagm = 1
                    xagm=xply+20
                    yagm=yply-50


                #上げミサイル発射上昇中か
                if fagm==1:
                    #上げミサイル描画
                    yagm -= 10
                    if yagm  >20:
                        fh5=agm(sc,xagm,yagm)
                        #agmミサイルがシェルターにヒットなら消す
                        if fh5==1:
                            fagm=0
                            fspky=0

                    else:#20以下なら消去
                        fagm=0


            #end(if fh2==0: 当たっていなければ以下

            #Gメモリ表示
            pygame.display.update()

            #イベント　キーボード取得
            for event in pygame.event.get(): 
                if event.type == QUIT: 
                    pygame. quit() 
                    sys. exit()
                elif event.type == KEYDOWN: 
                    if event.key==K_LEFT:
                      vply =-5
                    elif event.key==K_RIGHT:
                      vply =+5
                    elif event.key==K_SPACE:
                      fspky = 1
                      fh=0
    
    
                """
                elif event.type == MOUSEBUTTONUP: 
                  
                    if event.button==4:
                      print("wheel up")
                      whel +=1 
    
                    elif event.button==5:
                      print("wheel down")
                      whel -=1 
                      if whel <=1:
                        whel=1
    
                 """
            elapsed_time =( time.time() - start)*1000
            print ("elapsed_time:{0}".format(elapsed_time) + "[msec]")
            ck.tick(30) #毎秒30フレーム
    
        #end（while True:１フレーム

        if left_inv==0:
            break

        #やられたときの画面チカチカ
        for i in range(4):
            ck.tick(10) 
            pygame.display.update()
            sc.fill(( 0, 0,0))

            ck.tick(10) 
            pygame.display.update()
            sc.fill(( 255, 255, 255))

        #砲台残りが0か
        if left_ply ==0:
            break#あなたの負け

    #end（while True:砲台１つぶん

    if left_inv==0: #インベーダーを全部やっつけたか
        sc.fill(( 0, 0,255))
        #勝ち表示
        mm="あなたの勝ち"
        
        tm = mf2.render(mm, False,(0,0,0))
        sc.blit(tm,(200,100))

    
    if left_ply == 0: #砲台が0か
        sc.fill(( 255, 0,0))
        #負け表示
        mm="あなたの負け"
        tm = mf2.render(mm, False,(0,0,0))
        sc.blit(tm,(200,100))


    pygame.display.update()
    ck.tick(0.2) #５秒停止
    pygame.display.update()

#end（def main():


if __name__ == '__main__': main()

