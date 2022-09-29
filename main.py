import time;
import random;
field_opponent,field_player,ships_o,ships_p=[],[],[],[];
p_ship,x_sea,s_type=[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0];
iter=0;
for i in range(0,36):                                               #Собираем игровые поля
    field_opponent.append("o");
    field_player.append("o");
class Ship:                                                     #Класс кораблей:
    def __init__(self,x,y,type,h_v):
        self.x,self.y=int(x),int(y);                            # начальные координаты, левая верхняя точка
        self.type,self.h_v=int(type),int(h_v);                  # "клеточность" (1/2/3) и расположение (1/6)
    def SetShip(self):
        ship_array=[];
        if ((self.type==1 and s_type[self.type]==4)
        or (self.type==2 and s_type[self.type]==2)
        or (self.type==3 and s_type[self.type]==1)):
            raise TypeError("Too much ships of the same type");
            return False;
        point=self.x*self.y-1+(6-self.y)*(self.x-1);            # вычисление начальной точки корабля в игровом поле..
        self.h_v=6 if self.h_v==2 else 1;                       # ..с полученными координатами
        for i in range(0,self.type):
            ship_array.append(point);
            point+=self.h_v;                                    # следующая точка, в зависимости от ориентации корабля
        return ship_array;                                      # ... и возвращаем набор точек (без проверки)
class Sea:                                                                  # Класс игрового поля:
    tmp_f=[];
    def __init__(self, cells, owner):
        self.cells,self.owner=cells,owner;                                  #Координаты всех точек корабля
    def SetCells(self):
        tmp_f = field_player.copy() if self.owner == 1 else field_opponent.copy();
        for i in range(0,len(self.cells)):                                  # сперва запустим цикл только для проверки..
            if (self.cells[i]>35 or
            ((self.cells[i]+1)%6==0 and i!=(len(self.cells)-1)
            and (self.cells[i+1]-self.cells[i])==1)):                       # ..позиции на поле и возможных коллизий
                raise ValueError("Your new ship did not hit the sea");
                return False;
            if (tmp_f[self.cells[i]]=="\u25a0"):
                raise FloatingPointError("Ship collision prevented");
                return False;
            if ((self.cells[i]>0 and tmp_f[self.cells[i]-1]=="\u25a0"
            and self.cells[i]%6!=0)
            or (self.cells[i]<35 and tmp_f[self.cells[i]+1]=="\u25a0"
            and (self.cells[i]+1)%6!=0)
            or (self.cells[i]<30 and tmp_f[self.cells[i]+6]=="\u25a0")
            or (self.cells[i]>5 and tmp_f[self.cells[i]-6]=="\u25a0")):
                raise OverflowError("Too much ships in the same area");
                return False;
        tmp_f=[];
        for n in range(0, len(self.cells)):                                 # Если все нормально - ставим корабль на поле
            if self.owner==1:
                field_player[self.cells[n]]="\u25a0";                       # ..на поле игрока
            else:
                field_opponent[self.cells[n]]="\u25a0";                     # ..на поле ПК
            tmp_f.append(self.cells[n]);
        if self.owner == 1:
            s_type[len(self.cells)]+=1;                                     # Пополним перечень использованных кораблей
            ships_p.append(tmp_f);
        else:
            ships_o.append(tmp_f);
def disp():                                                                     # Программа показа игровых полей
    t,a,s,f="Ваше поле:"+" "*26+"Моё поле:\n"," ","|",1;
    for i in range(0,16):                                                       # Делаем верхнюю строку...
        t+=" "+str(a)+" "+str(s);
        if (5<i<8):
            a=s=" ";
            f=1;
        elif (i==8):
            s="|";
        else:
            a,s=f,"|";
            f+=1;
    t+="\n";
    spl=spc=1;                                                                  # ..и начинаем делать основное поле
    ro_pl=ro_pc=nn=0;
    enemy="";
    for i in range(0,84):
        if spl==spc:
            t+=" "+str(spl)+ " |";
            spl+=1;
        else:
            if nn<6:
                t += " " + str(field_player[ro_pl]) + " |";
                ro_pl+=1;
                nn+=1;
            elif nn==6:
                t+="         "+str(spc)+ " |";
                nn+=1;
            else:
                enemy="o" if field_opponent[ro_pc]=="\u25a0" else field_opponent[ro_pc];# скрываем корабли ПК

                t += " " + str(enemy) + " |";
                ro_pc+=1;
                nn+=1;
                if nn>12:
                    nn=0;
                    t+="\n";
                    spc+=1;
    print(t,end="");                                                                    # и выводим все поля в консоль
def init():                                                                             # Расстановка кораблей игроком
    err_t,w="",0;
    words=["Первый","Второй","Третий","Четвёртый","Пятый","Шестой","Седьмой"];
    while w < len(words):
        print("\n"*10,end="");
        print(err_t);                                                                   # Тут выводим ошибку, если есть
        disp();                                                                         # Покажем игровое поле
        if w==0:                                                                        # Первый ход
            print("Расставьте свои корабли. Есть три типа кораблей: 1,2 или 3 клетки."
                  "Горизонтальное(1) или вертикальное(2) расположение.\nПишется так: "
                  "строка-столбец-тип-ориентация, например: 1-1-3-1. Всего 7 кораблей: "
                  "четыре одноклеточных, два двухклеточных и один трёхклеточный.");
        try:                                                                            # Ловим исключения
            ans=input(f"{words[w]} корабль: ");
        except KeyboardInterrupt:
            print("\n\n\n\n\n\n\n\n\n\nКажется, Вы не окончили игру.");
            exit(0);
        if (len(ans)!=7 or (not (str(ans[0])+str(ans[2])+str(ans[4])+str(ans[6])).isdigit())
            or int(ans[0])<1 or int(ans[0])>6 or int(ans[2])>6 or int(ans[2])<1 or (int(ans[4]) not in (1,2,3))
            or (int(ans[6]) not in (1,2)) or (ans[1] or ans[3] or ans[5])!="-"):
            print ("\n"*10);
            err_t=("\n - - Неверно оформлен ввод: ошибка при создании корабля. Ещё раз (формат строка-стоблец-тип-положение).");
        else:
            print("\n" * 10);
            disp();
            p_ship[w]=Ship(ans[0],ans[2],ans[4],ans[6]);
            try:
                err_t ="";
                x_sea[w]=Sea(p_ship[w].SetShip(),1);                                    # Пробуем создать корабль
            except TypeError:
                err_t=(f"\n - - На поле уже достаточно кораблей {ans[4]}-го типа. Еще раз.");
                w -= 1;
            else:
                try:
                    x_sea[w].SetCells();                                                # Пробуем поставить корабль на доску
                except ValueError:
                    err_t=("\n - - Ваш новый корабль вышел за пределы игрового поля. Ещё раз.");
                    w-=1;
                except FloatingPointError:
                    err_t=("\n - - Координаты нового корабля совпадают с координатами уже существующего. Ещё раз.");
                    w-=1;
                except OverflowError:
                    err_t=("\n - - Новый корабль размещён слишком близко с другому кораблю. Ещё раз.");
                    w-=1;
            w+=1;
def pc_set():                                                           # Программа расстановки кораблей для ПК
    d=0;
    global iter;                                                        # Посчитаем, сколько попыток это у него займёт
    while d<7:                                                          # Всего 7 кораблей. Переберём все типы..
        iter+=1;
        x=random.randint(1,6);                                          # Координаты наугад. Если не получится поставить..
        y=random.randint(1,6);                                          # ..то мы вернемся сюда, и попробуем снова
        if d==0:
            t=3;                                                        # указываем тип
        elif 0<d<3:
            t=2;
        else:
            t=1;
        p=random.randint(1,2);                                          # указываем горизонталь / вертикаль
        p_ship[d] = Ship(x,y,t,p);                                      # генерируем клетки корабля...
        x_sea[d] = Sea(p_ship[d].SetShip(), 2);
        try:                                                            # Исключения естественно ловим без прерываний
            x_sea[d].SetCells();                                        # пробуем поставить новый корабль на поле
        except ValueError:
            None;                                                       # В случае ошибки - ничего не делаем -
        except FloatingPointError:                                      # - просто пробуем поставить корабль ещё раз
            None;
        except OverflowError:
            None;
        else:
            d+=1;
        if iter>500:                                                    # 500 попыток должо хватить
            break;
def rep(fld,plr):                                                           # Занесение 'следа залпа' на нужное поле
    global field_player,field_opponent;
    if plr==1:
        field_opponent=fld;
    else:
        field_player=fld;
def fire(plr):                                                              # Программа хода (и игрок и ПК)
    a=b=inp=hitp=inx=0;
    points,h_arr=[],[];
    target_f = field_player.copy() if plr == 2 else field_opponent.copy();  # Указываем, чьё поле будем 'обстреливать'
    if plr==2:                                                              # Если играет ПК ..
        for p in range (0,36):
            if target_f[p] in ("o","\u25a0"):
                points.append(p);                                           # .. собераем список возможных ходов (индекс)
        inp=random.choice(points);                                          # Стреляем наугад (из 'безошибочного' списка)
        a=(inp//6)+1;                                                       # Переводим индекс в читабельные координаты
        b=inp+7-a*6;
        inp=str(a)+"-"+str(b);
        time.sleep(1);                                                      # Сделаем задержку
        print(f"\n\n\nМой ход",end="");
        time.sleep(1);
        print(f" - {inp} - - - ...",end="");
        time.sleep(1);                                                      # Дальше ПК 'стреляет' так же, как игрок
    while True:
        if plr==1:
            time.sleep(1);
            try:                                                            # Остановка программы при запросе ввода..
                inp = input("Введите коориднаты:");                         # ..вызывает исключение. -
            except KeyboardInterrupt:                                       # - отловим его.
                print("\n\n\n\n\n\n\n\n\n\nКажется, Вы не окончили игру.");
                exit(0);
        if (len(inp) != 3 or (not (str(inp[0]) + str(inp[2])).isdigit()) or int(inp[0]) < 1
            or int(inp[0]) > 6 or int(inp[2]) > 6 or int(inp[2]) < 1 or inp[1] != "-"):
            print("\n - - Неверно оформлен ввод: ошибка координат. Ещё раз (формат строка-стоблец).");
            disp();
            return 1;
        else:
            x,y=int(inp[0]),int(inp[2]);
            hitp = x * y - 1 + (6 - y) * (x - 1);                           # Переведём координаты в индекс игрового поля
            if (target_f[hitp] in ("T","X")) and plr==1:
                print(f"\n - - В эту область (строка {x} столбец {y}) вы уже стреляли. Ещё раз.");
                disp();
                return 1;
            elif target_f[hitp]=="o":
                if plr==1:
                    print("\n\n\n");
                print("!!!! МИМО !!!!");
                target_f[hitp]="T";
                rep(target_f, plr);                                     # Не попал - запишем это на поле игрока 'plr'
                disp();
                return 2 if plr==1 else 1;                              # Передаем право хода следующему игроку
            else:                                                       # В случае, если есть попадание в корабль...
                for i in range(0,7):                                    # (и тут начнем перебирать коллекции кораблей)
                    target_f[hitp] = "X";                               # ..отметим это на временном поле..
                    rep(target_f, plr);                                 # ..и перенесем его на поле реальное
                    a=len(ships_o[i]) if plr==1 else len(ships_p[i])
                    for n in range(0,a):                                # Переберём все клеточки конкретного корабля..
                        if (plr==1 and ships_o[i][n]==hitp) or (plr==2 and ships_p[i][n]==hitp):
                            if plr==1:
                                ships_o[i][n]="X";                      # И если он подбит, отметим это в "коллекциии"
                            else:
                                ships_p[i][n] = "X";
                            if (plr==1 and ships_o[i].count("X")!=a) or (plr==2 and ships_p[i].count("X")!=a):
                                if plr == 1:
                                    print("\n\n\n");
                                print (f"!!!! ЕСТЬ ПОПАДАНИЕ !!!!");
                                disp();
                                return 1 if plr==1 else 2;              # Сохраняем право хода текущего игрока
                            else:                                       # А если мы видим, что в коллекции кораблей..
                                if plr == 1:                            # ..все клетки корабля 'помечены', то становится..
                                    print("\n\n\n");                    # ..понятно, что корабль потоплен
                                    print(f"!!!! КОРАБЛЬ {len(ships_o[i])}-ГО ТИПА ПОТОПЛЕН !!!!");
                                else:
                                    print(f"!!!! КОРАБЛЬ {len(ships_p[i])}-ГО ТИПА ПОТОПЛЕН !!!!");
                                disp();
                                return 1 if plr==1 else 2;              # Дадим возможность текущему игроку доиграть
def game():
    plr=1;
    while True:
        plr=fire(plr);                                              # Рарзешим сделать 'залп' текущему игроку
        if field_opponent.count("X")==11:                           # В случае победы игрока:
            print(" - - - - - Вы потопили все мои корабли. Победа за Вами. Игра окончена. - - - - -",end="");
            exit(0);
        if field_player.count("X")==11:                             # В случае победы ПК:
            print(" - - - - - Я потопил все Ваши корабли. Больше у Вас ничего нет. Игра окончена. - - - - -",end="");
            exit(0);
init();                                                             # Начало. Сперва дадим игроку расставить корабли
print("\n"*10);
disp();
s_type=[0,0,0,0];                                                   # Подчистим список использованных кораблей ..
pc_set();                                                           # .. и дадим ПК расставить свои корабли
print("\n"*20);
disp();
if iter>500:                                                        # На случай критической неудачи
    print("Я тоже попытался расставить свои корабли. Но не смог.\nПрограмма завершена.");
    exit(0);
else:
    print(f"Я тоже расставил свои корабли. Количество попыток расстановки - {iter}. Теперь Ваш ход (строка-столбец).");
game();                                                             # Переходим к игре. Начнем делать ходы