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
msgothic = r'c:\windows\fonts\msgothic.ttc'
mf = pygame.font.Font(msgothic, 24)
mf2= pygame.font.Font(msgothic, 48)

# サウンドをロード
sd_hit = pygame.mixer.Sound("hit.wav")
sd_heli = pygame.mixer.Sound("shot.wav")
#sd_shot = pygame.mixer.Sound("shot.wav")
sd_bomb = pygame.mixer.Sound("bomb.wav")
#        sd_heli.play()

#シェルター行列
tb_shl =[[[1 for i in range(5)] for j in range(3)] for k in range(4)]

for i in range(4):
    tb_shl[i][2][2]=0
    tb_shl[i][0][0]=0
    tb_shl[i][0][4]=0

#インベーダー行列
tb_inv = [[1 for i in range(8)] for j in range(4)]



class disp():	
    #得点表示用
    msgothic = r'c:\windows\fonts\msgothic.ttc'
    mf = pygame.font.Font(msgothic, 24)
    mf2 = pygame.font.Font(msgothic, 48)
    point=0

    #得点や砲台残り表示
    def drawpoint(self,left_ply,left_inv):
        #砲台残り表示
        mm="Point="+str(self.point)+"   砲台="+str(left_ply)+"  invader "+str(left_inv)
        tm = self.mf.render(mm, False,(0,0,0))
        sc.blit(tm,(150,10)) 

    #得点や砲台残り表示
    def dbg(self,mm):
        #mm="Point="+str(self.point)+"   砲台="+str(left_ply)+"  invader "+str(left_inv)
        tm = self.mf.render(mm, False,(0,0,0))
        sc.blit(tm,(450,70)) 

#インベーダー
class invader():


    #アイコン
    giv1 = pygame.image.load("invader1.png").convert_alpha()#インベーダー　　50x50
    giv2 = pygame.image.load("invader2.png").convert_alpha()#インベーダー２　50x50

    ct=0    #カウンタ　10fps(fpsct) になるごとにインベーダを動かす
    fpsct=0  #何カウントで動かすか
    anm_inv=0 #インベーダーの手の上げ下げ

    xinv=0
    yinv=0
    vinv=0

    xrlim=700   #折り返す右端
    xllim=100   #

    left_inv=0
    min=0
    max=0

    #インヴェーダのコンストラクタ
    def __init__(self):

        #インヴェーダの位置
        self.xinv=102
        self.yinv=50

        #インヴェーダの速度
        self.vinv=2

        #インヴェーダの残り
        self.left_inv=32

        #インヴェーダの横方向の長さ
        self.min=0
        self.max=7

        self.fpsct=10

    #def calcinvader(self):
    def calcinvader(self):
        #インベーダー スピード調節　後半早くする
        #　　最後の一匹　激速

        #残り数が減ってきたらスピードアップ
        if self.left_inv <10:
            #5fpsで動かす,もともとインベーダは10fpsごとに動かしていた
            self.fpsct=5 
            if self.vinv>0:
                self.vinv = 4
            else:
                self.vinv= -4

        if self.left_inv ==1:
            self.fpsct=1 #1fpsで動かす
            if self.vinv>0:
                self.vinv = 14
            else:
                self.vinv= -14


        self.ct+=1
        if self.ct>self.fpsct:#内部クロック10フレームに一回、全体を動かす

            self.ct=0
            self.xinv += self.vinv

            #全体長チェック
            self.min,self.max=self.chklen() 

            #画面の右端de折り返す
            if self.xinv+self.max*70>self.xrlim-60:
                #import pdb;pdb.set_trace() #debug
                self.vinv *=-1
                self.yinv +=10
                
            #画面の左端なら右に折り返す
            elif self.xinv+self.min*70 <self.xllim:
                #import pdb;pdb.set_trace() #debug
                self.vinv *=-1
                self.yinv +=10

            #end (if else

            #手を上げたり下げたりアニメのためのフラグ
            self.anm_inv +=1
            if self.anm_inv==2:
                self.anm_inv=0

        #インベーダーの描画　動かすのは10カウントに1回だが描画は毎回やる
        #　そうしないと消えた感じがする
        self.drawinvader()

        #インベーダーの総数をカウント
        self.left_inv=self.chknum()


    #終了　def calcinvader(self):

    
    #インベーダー描画　（インベーダー行列tb_inv　にしたがって1なら描画
    def drawinvader(self):
      for y in range (4):#横5行
        for x in range (8):#縦8個
    
          #行列中、x,yのインベーダが生きているなら以下実行
          if tb_inv[y][x]==1:#生きている
    
            #インベーダの座標
            ix=self.xinv+x*70
            iy=self.yinv+y*60

            #インヴェーダの描画（メモリ書き込み）
            if self.anm_inv==1:
                sc.blit(self.giv1, Rect(ix,iy,50,50))
    
            else:
                sc.blit(self.giv2, Rect(ix,iy,50,50))
    
            #end(if anm_inv==1:
          #--end (if tb_inv[x,y]==1:
        #end (for x in range (0,8):
      #end(for y in range (0,4):


    def chknum(self):
    #インベーダの数の計測
        num=0
        for tx in range(8):
            for ty in range(4):
                if tb_inv[ty][tx]==1:
                    num +=1
        return num


    def chklen(self):
    #インベーダの全体の長さの計測　
        xl_inv=70*8
        sum=[0]*8
    
        for tx in range(8):
            for ty in range(4):
                sum[tx] +=tb_inv[ty][tx]
    
        #ここからは最小値、最大値を求める問題
        #左端から最初に0以外が来るまで
        self.min=0
        for tx in range(8):
            if sum[tx]>0:
                self.min=tx
                break
    
        #右端から最初に0以外が来るまで
        self.max=7
        for tx in reversed(range(8)):
            if sum[tx]>0:
                self.max=tx
                #import pdb;pdb.set_trace() #debug
                break
    
        return self.min,self.max




#プレイヤー
class player():


    #砲台　　　　　　　50x50
    gply = pygame.image.load("player.png").convert_alpha()
    vply=0
    xply=0
    yply=0
    left_ply=0

    #クラス内フラグ
    fspky=0


    def __init__(self):
        self.xply=400
        self.yply=500
        self.fspky=0
        self.left_ply=3

    def res_player(self):
        self.xply=400
        self.yply=500
        self.fspky=0
        self.drawplayer()

    #def calcplayer(self,left_ply,fagm):
    def calcplayer(self,fl):
        #  return fagm,xag,yagm

        #キー読み込み
        self.getkey()

        #x位置更新
        self.xply += self.vply
        if self.xply>650:
            self.xply=650
        elif self.xply <50:
            self.xply=50

        #砲台表示（書き込み）
        self.drawplayer()

        #あげミサイル発射
        #スペースキーが押され　fspky=1　
        #　かつ上げミサイルが未発射　fagm==0　なら
        if self.fspky==1 and fl.fagm==0:
            sd_hit.play()#サウンドhit

            #上げミサイルフラグオン、砲台の位置をagmの初期としてセット
            fl.agm=1
            fl.xagm=self.xply+20
            fl.yagm=self.yply-50
            fl.f1agm=1

        else:
            fl.agm=0
            fl.xagm=0
            fl.yagm=0
            fl.f1agm=0

        return fl

    def drawplayer(self):
        sc.blit(self.gply ,Rect(self.xply,self.yply,50,50))

    #イベント　キーボード取得
    def getkey(self):
        self.fspky=0
        for event in pygame.event.get(): 
            if event.type == QUIT: 
                pygame. quit() 
                sys. exit()
            elif event.type == KEYDOWN: 
                if event.key==K_LEFT:
                  self.vply =-5
                elif event.key==K_RIGHT:
                  self.vply =+5
                elif event.key==K_SPACE:
                  self.fspky = 1
                  #self.fh=0

#end class plyer():




#上げミサイル
class agm(disp):#()内は引数じゃなくて親クラス　dispクラスのメソッドを使う

    #agmミサイル　　　　　20x50
    gagm = pygame.image.load("age.png").convert_alpha()
    xagm=0
    yagm=0

    def __init__(self,fl):
        self.xagm=fl.xagm
        self.yagm=fl.yagm


    def calcagm(self,fl,xinv,yinv,bs,point):
    #    return fl,point,fboss

        #agmミサイル位置更新
        self.yagm -= 10
        if self.yagm > 20:
            #agmミサイル描画（画像メモリ書き込み
            self.drawagm()

            #agmミサイルがシェルターにヒットかチェック
            fh_agm_shl=self.chk_hit_shl()
            #agmミサイルがシェルターにヒットならagm消す
            if fh_agm_shl==1:
                fl.fagm=0

            #agmミサイルがインベーダーにヒットかチェック
            fh_agm_inv,fpt=self.chk_hit_inv(xinv,yinv)
            #agmミサイルがインベーダーにヒットならagm消す
            if fh_agm_inv==1:
                fl.fagm=0
                point+=10*fpt

            #agmミサイルがボスにヒットかチェック
            fh_agm_boss=self.chk_hit_boss(bs.xboss,bs.yboss)
  
            #agmミサイルがボスにヒットならagm消す
            if fh_agm_boss==1:
                fl.fagm=0
                point+=100 #得点
                sd_bomb.play()
                bs.xboss=0 #ボスも消す
                bs.fboss=0 

        else:#agmミサイルが画面の上に来た（yagmが20以下）なら消去
            fl.fagm=0

        return fl,point

    #end(calcagm():


    #上げミサイル描画
    def drawagm(self):
        sc.blit(self.gagm ,Rect(self.xagm,self.yagm,20,50))


    #agmがシェルターと当たっているかチェック
    def chk_hit_shl(self):

        fh_agm_shl=0

        #戻り値　当たりフラグ１つ、グローバル変数変更　tb_shl[][][]
        for tk in range (4):
            dx=self.xagm-(120+tk*150)
            if -10 < dx and dx < 90: #x当たり
                dy=350-self.yagm
                if -40 < dy and dy<30: #y当たり
                    ix=int((dx+10)/20)
                    iy=int(dy/20)

                    if tb_shl[tk][iy][ix] ==1: #真のあたり
 
                        tb_shl[tk][iy][ix] =0
                        fh_agm_shl=1
                        #import pdb;pdb.set_trace() #debug


        return fh_agm_shl


    #agmがインベーダーと当たっているかチェック
    def chk_hit_inv(self,xinv,yinv):
        #戻り値　fh_agm_inv 当たりフラグ１つ、グローバル変数変更　tb_inv[iy][ix]

        fh_agm_inv=0
        fpt=0
        for ix in range(8):
            tx=xinv+ix*70
            dx=self.xagm-tx
            if -20<dx and dx <50: #xだけ当たり
                for iy in range(4):
                    ty=yinv+iy*60
                    dy=self.yagm-ty
                    if 0<dy and dy <50 :#yだけ当たり
                        if tb_inv[iy][ix] ==1: #真のあたり
                            tb_inv[iy][ix] =0
                            fh_agm_inv=1
                            fpt=4-iy
                    #import pdb;pdb.set_trace() #debug
        return fh_agm_inv,fpt

    #agmがボスと当たっているかチェック
    def chk_hit_boss(self,xboss,yboss):
        #戻り値　fh_agm_boss 当たりフラグ１つ

        fh_agm_boss=0

        dy=self.yagm-yboss
        if 0<dy and dy <60 :#yだけ当たり

            dx=self.xagm-xboss
            if -2<dx and dx <70: #xだけ当たり
                fh_agm_boss=1
                #import pdb;pdb.set_trace() #debug

        return fh_agm_boss

#end agm():




#シェルター
class shelter():

    #シェルター　　　　20x20
    gsh1 = pygame.image.load("sh_blk.png").convert_alpha()
    gsh2 = pygame.image.load("sh_blk2.png").convert_alpha()#残骸
    gsh3 = pygame.image.load("sh_blk3.png").convert_alpha()#残骸
    gsh4 = pygame.image.load("sh_blk4.png").convert_alpha()#残骸

    
#    def __init__():
#        pass

    #シェルター描画　４つ分
    #shelter　当たり判定
    def drawshelter(self):
    
        #import pdb;pdb.set_trace() #debug
        for tk in range(4): #0,1,2,3
          for ty in range(3): #0,1,2
            for tx in range(5): #0,1,2,3,4
               ttx=120+tk*150
               tty=350
    
               #tr=random.randint(0,10)
               if tb_shl[tk][ty][tx]==1:
                   #シェルター描画　レンガ１つ分
                   sc.blit(self.gsh1 ,Rect(ttx+tx*20,tty+ty*20,20,20))
    
               else:#残骸　or　何も書かない
                   if ty==0:
                       if tb_shl[tk][1][tx]==0:
                           pass
                       else:
                           sc.blit(self.gsh3 ,Rect(ttx+tx*20,tty+ty*20,20,20))
                   elif ty==1:
                       if tb_shl[tk][2][tx]==0:
                           pass
                       else:
                           sc.blit(self.gsh2 ,Rect(ttx+tx*20,tty+ty*20,20,20))
                   else:#ty=2
                       if tb_shl[tk][1][tx]==0:
                           pass
                       else:
                           sc.blit(self.gsh4 ,Rect(ttx+tx*20,tty+ty*20,20,20))




#sgmミサイル
class sgm():

    #sgmミサイル　　　　　20x50
    gsgm = pygame.image.load("oti.png").convert_alpha()

    #sgmミサイルのフラグ、1飛んでいる 0ぶつかった
    fsgm=0
    #位置
    xsgm=0
    ysgm=0


    def __init__(self,xsgm,ysgm,fsgm):
        self.fsgm=1     # 1:生きている　0:シェルタにあたった　-1:砲台に当たった
        self.xsgm=xsgm
        self.ysgm=ysgm


    #sgmミサイル計算
    def calcsgm(self,xply,yply):

        #下げミサイル位置更新
        self.ysgm += 10
        self.drawsgm()
     
        #下げミサイルの位置が550以上なら削除
        if self.ysgm> 500:
            self.fsgm=0

        #下げミサイルがシェルタに当っていれば行列から削除
        fh_sgm_shl=self.chk_hit_shl()

        if fh_sgm_shl==1:
            #import pdb;pdb.set_trace() #debug
            self.fsgm=0

        #下げミサイルが砲台（プレイや）に当っていればfsgm　マイナス
        fh_sgm_ply=self.chk_hit_ply(xply,yply)

        if fh_sgm_ply==1:
            #import pdb;pdb.set_trace() #debug
            self.fsgm=-1

        return self.fsgm
    #end(下げミサイル

    #sgmミサイル描画
    def drawsgm(self):
        sc.blit(self.gsgm ,Rect(self.xsgm,self.ysgm,5,20))

    #砲台と当たっているかチェック
    def chk_hit_ply(self,xply,yply):
        fh_sgm_ply=0
        #import pdb;pdb.set_trace() #debug

        tx=self.xsgm-xply
        if -2 < tx and tx <34: #x当たり
            ty=math.fabs(self.ysgm-yply)
            #import pdb;pdb.set_trace() #debug

            if ty<20: #当たり
                #import pdb;pdb.set_trace() #debug
                fh_sgm_ply=1
        return fh_sgm_ply
    
    #シェルターと当たっているかチェック
    def chk_hit_shl(self):
        fh_sgm_shl=0
        for tk in range (4):
            dx=self.xsgm-(120+tk*150)
            if -10 < dx and dx < 90: #x当たり
                dy=350-self.ysgm
                if -40 < dy and dy<30: #y当たり
                    ix=int((dx+10)/20)
                    iy=int((dy-10)/20)
    
                    if tb_shl[tk][iy][ix] ==1: #真のあたり
     
                        tb_shl[tk][iy][ix] =0
                        fh_sgm_shl=1
    
        return fh_sgm_shl

class flag():
        xagm=0
        yagm=0
        fsgm=0    #sgm発生か　yesなら１
        fagm=0    #0:未発射  1:発射後　上昇中
        f1agm=0

#ボス
class boss():
    gbs1 = pygame.image.load("boss1.png").convert_alpha()#boss　　50x50
    gbs2 = pygame.image.load("boss2.png").convert_alpha()#boss２　50x50

    xboss=0
    yboss=0
    fboss=0
    vboss=0
    anm_boss=0

    def start(self,xs):

        self.xboss=xs
        self.yboss=20
        self.anm_boss=0  #for anime
        self.fboss=1
        #self.vboss=1


    def calcboss(self):
        #ボスのx位置更新
        self.xboss += self.vboss

        #ボスの描画
        self.drawboss()

        #端っこまで移動したか
        if self.xboss>800 or self.xboss < -50:
            rboss=1      #端っこまで移動フラグ　1
            self.fboss=0
        else:
            rboss=0
            #self.fboss=1

        return rboss

    #ボスの描画（メモリ書き込み）
    def drawboss(self):

        #アニメフラグが1,0のどちらか
        self.anm_boss +=1
        if self.anm_boss>1:
            self.anm_boss=0

        #描画（メモリ書き込み）
        if self.anm_boss==1:
            sc.blit(self.gbs1, Rect(self.xboss,self.yboss,50,50))
            #sd_heli.play()

        else:
            sc.blit(self.gbs2, Rect(self.xboss,self.yboss,50,50))

#ここまでクラス定義
#----------------------------------------------------------------
#ここから関数

def movie(ck):
            #映画効果用
            start = time.time() #1フレームの時間測定　16msec以内ならOK

            sc.fill(( 0, 0, 0))
            #Gメモリ表示
            pygame.display.update()
            #時間調整　16.7msecになるまで待つ
            ck.tick(60) #毎秒30フレーム

            #1フレームの時間表示
            elapsed_time =( time.time() - start)*1000
            print ("elapsed_time xxx:{0}".format(elapsed_time) + "[msec]")


#下げミサイル発生
def gen_sgm(sg,iv):
    #乱数が一定以上なら　sgm発生
    rr=random.random()
    if rr<0.2:
        rx=random.randint(0,7)
        ry=random.randint(0,3)
        #ソノ位置のインベーダーが生きているならsgm発生
        if tb_inv[ry][rx]==1:
           fsgm=1
           xsgm=iv.xinv+rx*70+20
           ysgm=iv.yinv+ry*60+20
           sg.append(sgm(xsgm,ysgm,fsgm))#sgm発生（コンストラクタ

#下げミサイル削除
def del_sgm(sg,pl):
    fh_sgm_ply=0#砲台に当たっているか
    #forループ内で配列sg[]を消すのでケツから回している
    for i in reversed(range(len(sg))):
        fsgm=sg[i].calcsgm(pl.xply,pl.yply)
        #fsgmがセロかマイナスなら消去
        if fsgm<=0:
            sg.pop(i)#SGM消去

        if fsgm==-1:
            fh_sgm_ply=1#砲台に当たっていたら一旦終了

    return fh_sgm_ply



def plpl(fl,pl):
    fl=pl.calcplayer(fl)
    if fl.f1agm==1:  #fagm との違いに注意！
                    #fagmはミサイルが上がっている間１
                    #f1agmはスペースキーが押された瞬間だけ１
                    #わけないと何発でもagmを発射してしまう
        ag=agm(fl)   #agm発生　コンストラクタ
        fl.f1agm=0   #f1agmはスペースキーが押された瞬間だけ１なのですぐ戻す
        fl.fagm=1    #fagmはミサイルが上がっている間１

    return fl,ag

#ボスの処理
def bossmain(bs):

    r1=random.random()
    #boss発生　0.5%の確率で
    if r1<0.005  and bs.fboss==0:
        bs.fboss=1 #発生ならフラグ１
        r2=random.random()#右から出るか左から出るか
        r3=random.randint(2,7)#ボスのスピードを決定

        if r2<0.5 :
            tx=700 #左端からスタート
            bs.vboss=r3*-1 #ボスのスピード
        else:
            tx=0   #右端からスタート
            bs.vboss=r3 #ボスのスピード
        bs.start(tx) #ボス 初期設定

    if bs.fboss==1:
        rboss=bs.calcboss() #位置計算と描画
        #端っこまで移動してならrboss=1で戻る
        if rboss==1:
            bs.fboss=0



def hantei(iv,pl,ck):
    if iv.left_inv==0: #インベーダーを全部やっつけたか
        sc.fill(( 0, 0,255))
        #勝ち表示
        mm="YOU ARE WINNER!!"
        
        tm = mf2.render(mm, False,(0,0,0))
        sc.blit(tm,(200,100))

    
    if pl.left_ply == 0: #砲台が0か
        sc.fill(( 255, 0,0))
        #負け表示
        mm="あんたの負けずら"
        tm = mf2.render(mm, False,(0,0,0))
        sc.blit(tm,(200,100))

    pygame.display.update()
    ck.tick(0.5) #５秒停止
    pygame.display.update()


def tikatika(ck):
    for i in range(4):
        ck.tick(10) 
        pygame.display.update()
        sc.fill(( 0, 0,0))

        ck.tick(10) 
        pygame.display.update()
        sc.fill(( 255, 255, 255))


def main():
    # BGMを再生
    #pygame.mixer.music.load("tam-n11.mp3")
    #pygame.mixer.music.play(-1)

    ck = pygame.time.Clock()

    #class　インスタンス化、コンスタラクタ呼び出し
    dp=disp()
    sh=shelter()
    iv=invader()
    pl=player()
    bs=boss()

    #クラス用の配列準備 コンストラクタはここでは呼んでいない
    sg=[]#下げミサイル、

    while True:#砲台1つ分

        #砲台リスタート
        pl.res_player()

        #コミュニケーションflag
        fh_sgm_ply=0 	#sgm ミサイルが砲台にhitか　　
        fl=flag()# フラグまとめクラス　xagm,yagm,fsgm=0,fagm,f1agm=0

        while True:#1画面分　1フレーム
            #1フレームの時間測定　16msec以内ならOK
            start = time.time() 

            #画面クリア
            sc.fill(( 255, 255, 255))

            #invader
            iv.calcinvader()

            #plyer()
            
            fl=pl.calcplayer(fl)
            if fl.f1agm==1:  #fagm との違いに注意！
                             #fagmはミサイルが上がっている間１
                             #f1agmはスペースキーが押された瞬間だけ１
                             #わけないと何発でもagmを発射してしまう
                ag=agm(fl)   #agm発生　コンストラクタ
                fl.f1agm=0   #f1agmはスペースキーが押された瞬間だけ１なのですぐ戻す
                fl.fagm=1    #fagmはミサイルが上がっている間１
	    
            #sgm
            gen_sgm(sg,iv)
            fh_sgm_ply=del_sgm(sg,pl)

            #shelter
            sh.drawshelter()

            #boss
            bossmain(bs)

            #agm()
            if fl.fagm==1:
                fl,dp.point=ag.calcagm(fl,iv.xinv,iv.yinv,bs,dp.point)

            #ブレーク処理
            if fh_sgm_ply==1 or iv.left_inv==0:
                break

            #得点などの描画
            dp.drawpoint(pl.left_ply,iv.left_inv)

            #Gメモリ表示
            pygame.display.update()
            ck.tick(30) #毎秒30フレーム

            #1フレームの時間表示
            elapsed_time =( time.time() - start)*1000
            print ("elapsed_time:{0}".format(elapsed_time) + "[msec]")

            #映画効果用オプション
            #movie(ck)

        #end（while True:１フレーム

        #while True:１フレームを抜けた所
        #インベーダーの残りがゼロならばもう一回抜ける
        if iv.left_inv==0:
            break

        #そうでなければやられたときの画面チカチカ
        tikatika(ck)

        #砲台マイナスして残りが0か
        pl.left_ply -=1
        if pl.left_ply ==0:
            break#あなたの負け

    #end（while True:砲台１つぶん

    hantei(iv,pl,ck)

#end（def main():


if __name__ == '__main__': main()

