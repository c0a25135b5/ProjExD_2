import os
import pygame as pg
import random
import sys
import time


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP:(0, -5), 
    pg.K_DOWN:(0, 5), 
    pg.K_LEFT:(-5, 0), 
    pg.K_RIGHT:(5, 0),
    }
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rect: pg.Rect) -> tuple[bool, bool]:
    """
    引数:こうかとんRect or 爆弾Rect
    戻り値:横方向・縦方向の真理値タプル
    (True:画面内/False:画面外)
    """
    yoko, tate = True, True
    if rect.left < 0 or WIDTH < rect.right:
        yoko = False
    if rect.top < 0 or HEIGHT < rect.bottom:
        tate = False
    return yoko, tate


def gameover(screen: pg.Surface) -> None:
    """
    引数:スクリーンサーフェース
    戻り値:なし
    ゲームオーバー画面出力関数
    """
    bo_img = pg.Surface((1100, 650)) #  ブラックアウト画面
    pg.draw.rect(bo_img, (0, 0, 0), pg.Rect(0, 0, 1100, 650))
    bo_img.set_alpha(200)
    screen.blit(bo_img, [0, 0])
    fonto = pg.font.Font(None, 80)
    gameover_txt = fonto.render("Game Over", True, (255, 255, 255))
    screen.blit(gameover_txt, [400, 300])
    kk_crying_img = pg.image.load("fig/8.png")
    screen.blit(kk_crying_img, [300, 300])
    screen.blit(kk_crying_img, [800, 300])
    pg.display.update()
    time.sleep(5)


def get_kk_imgs() -> dict[tuple[int, int], pg.Surface]:
    """
    引数:なし
    戻り値:移動タプルに対応する画像Surface
    飛ぶ方向でこうかとんの画像が変わる
    """
    kk_img = pg.image.load("fig/3.png")
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_dict = {
        (0, 0): pg.transform.rotozoom(kk_img, 0, 1.0),
        (5, 0): pg.transform.rotozoom(pg.transform.flip(kk_img, True, False), 0, 1.0),
        (5, -5): pg.transform.rotozoom(pg.transform.flip(kk_img, True, False), 45, 1.0),
        (0, -5): pg.transform.rotozoom(pg.transform.flip(kk_img, True, False), 90, 1.0),
        (-5, -5): pg.transform.rotozoom(kk_img, -45, 1.0),
        (-5, 0): pg.transform.rotozoom(kk_img, 0, 1.0),
        (-5, 5): pg.transform.rotozoom(kk_img, 45, 1.0),
        (0, 5): pg.transform.rotozoom(pg.transform.flip(kk_img, True, False), -90, 1.0),
        (5, 5): pg.transform.rotozoom(pg.transform.flip(kk_img, True, False), -45, 1.0),
    }
    return kk_dict


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    vx, vy = 5, -5
    kk_imgs = get_kk_imgs()  
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0])

        if kk_rct.colliderect(bb_rct): #  issue1 真理値の無駄遣いを修正
            gameover(screen)
            return

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, tpl in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        kk_img = kk_imgs[tuple(sum_mv)]  
        screen.blit(kk_img, kk_rct)

        bb_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
