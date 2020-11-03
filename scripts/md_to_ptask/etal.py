import builtins

_g_print_list = []  
def _prepare_list():
    global _g_print_list
    _g_print_list = []
    
def _print_to_list(*args, **kwargs):
    global _g_print_list
    if len(args) != 1 or len(kwargs) != 0:
        _fatal('Некорректный формат печати в функции print. Должен быть только один аргумент, например: print("hello") или print(8.9).')
    _g_print_list.append(str(args[0]))
    
def _get_print_res(is_float_out):
    global _g_print_list
    if is_float_out:
       assert len(_g_print_list) == 1
       exp_float_s = '{:.2f}'.format(float(_g_print_list[0]))
       return exp_float_s
    return '\\n'.join(_g_print_list)

class CTask:
    """Класс для печати эталонной таблицы на основе входных данных"""
    def __init__(self,float_out=False,test_list=None):
        self._tl = test_list
        self._float_out = float_out
    def _run_test_list(self,num_args):
        out_list = []
        for a in self._tl:
            _prepare_list()
            if num_args == 1:
                self.main1(a)
            elif num_args == 2:
                self.main2(a[0],a[1])
            elif num_args == 3:
                self.main3(a[0],a[1],a[1])
            else:
                raise NotImplementedError
            res = _get_print_res(self._float_out)
            if num_args == 1:
                out_list.append('|{}|{}|'.format(a,res))
            elif num_args == 2:
                out_list.append('|{}|{}|{}|'.format(a[0],a[1],res))
            elif num_args == 3:
                out_list.append('|{}|{}|{}|{}|'.format(a[0],a[1],a[2],res))
        out_str = '\n'.join(out_list)
        return out_str
        
    def gen(self):
        original_print = print
        out_str = ''
        builtins.print = _print_to_list
        if test_list==None:
            _prepare_list()
            self.main0()
            res = _get_print_res(self._float_out)
            out_str = '|{}|'.format(res)
        else:
            assert len(test_list) >= 1
            if not isinstance(test_list[0],list):
                out_str = self._run_test_list(1)
            elif len(test_list[0])==2:
                out_str = self._run_test_list(2)
            elif len(test_list[0])==3:
                out_str = self._run_test_list(3)
            else:
                raise NotImplementedError
        builtins.print = original_print
        return out_str
    def main0(self):
        raise NotImplementedError
    def main1(self,a):
        raise NotImplementedError
    def main2(self,a,b):
        raise NotImplementedError
    def main3(self,a,b):
        raise NotImplementedError

#1.1
class p15(CTask):
    def main0(self):
        print(15)
        
class p3000(CTask):
    def main0(self):
        print(3000)

class ppi(CTask):
    def main0(self):
        print(3.14)

class pspace(CTask):
    def main0(self):
        print('1 13 49')

class pspace2(CTask):
    def main0(self):
        print('7  15  100')

class pcol(CTask):
    def main0(self):
        print(50)
        print(10)
    
class pcol2(CTask):
    def main0(self):
        print(5)
        print(10)
        print(21)
    
#1.2
class psquare(CTask):
    def main1(self,a):
        print(4*a)


class prect(CTask):
    def main2(self,a,b):
        print(a*b)
        print(2*(a+b))

class pcdel(CTask):
    def main1(self,s):
        print(s//100)

class pdes(CTask):
    def main1(self,num):
        print(num//10)
        print(num%10)

class psut(CTask):
    def main1(self,sec):
        print(sec//3600)

class phung(CTask):
    def main1(self,num):
        s = num//100
        d = (num//10)%10
        ed = num%100-d*10
        print(ed)
        print(d)
        print(s)

class prev(CTask):
    def main1(self,num):
        print(-num)

class pcube(CTask):
    def main1(self,lc):
        print(lc*lc*lc)
        print(lc*lc*4)

class pmid(CTask):
    def main2(self,n1,n2):
        print((n1+n2)//2)

class pcent(CTask):
    def main1(self,num):
        print(num//100)

class ptonn(CTask):
    def main1(self,num):
        print(num//1000)

class pweek(CTask):
    def main1(self,d):
        print(d//7)
#1.3
class pcircle(CTask):
    def main1(self,r):
        print(3.14*r*r)

class pfish(CTask):
    def main1(self,rub):
        print(rub + rub*0.12)

class prad(CTask):
    def main1(self,rad):
        print(rad*3.14/180)

class pdeg(CTask):
    def main1(self,deg):
        print(deg/3.14*180)
        
class phypo(CTask):
    def main2(self,k1,k2):
        print(k1*k1+k2*k2)
        
class pplot(CTask):
    def main2(self,v,m):
        print(m/v)
        
class pcity(CTask):
    def main2(self,cnt,s):
        print(cnt/s)

#1.4
class pruen(CTask):
    def main0(self):
        print('приветHELLO')
        
class pdoq(CTask):
    def main0(self):
        print('"ПРИВЕТ МИР"')
        
class poneq(CTask):
    def main0(self):
        print("'багет'")


if __name__=='__main__':
    test_spec=[
        #имя               класс   таблица теста   ответ - float
        {'name':'1.1.p15','tc':p15,'tt':None,'fl':False},
        {'name':'1.1.p300','tc':p3000,'tt':None,'fl':False},
        {'name':'1.1.pi','tc':ppi,'tt':None,'fl':False},
        {'name':'1.1.space','tc':pspace,'tt':None,'fl':False},
        {'name':'1.1.space2','tc':pspace2,'tt':None,'fl':False},
        {'name':'1.1.col','tc':pcol,'tt':None,'fl':False},
        {'name':'1.1.col2','tc':pcol2,'tt':None,'fl':False},
        
        {'name':'1.2.square','tc':psquare,'tt':[1,2,3,4],'fl':False},
        {'name':'1.2.rect','tc':prect,'tt':[[1,1],[10,2],[2,7]],'fl':False},
        {'name':'1.2.cdel','tc':pcdel,'tt':[100,101,349,699],'fl':False},
        {'name':'1.2.des','tc':pdes,'tt':[45,67,91],'fl':False},
        {'name':'1.2.sut','tc':psut,'tt':[3610,10890,55],'fl':False},
        {'name':'1.2.hung','tc':phung,'tt':[456,123,980],'fl':False},
        {'name':'1.2.rev','tc':prev,'tt':[-1,3,0],'fl':False},
        {'name':'1.2.cube','tc':pcube,'tt':[1,2,3],'fl':False},
        {'name':'1.2.mid','tc':pmid,'tt':[[45,47],[10,30],[90,110]],'fl':False},
        {'name':'1.2.cent','tc':pcent,'tt':[1234,654,54],'fl':False},
        {'name':'1.2.tonn','tc':ptonn,'tt':[4321,678909,999],'fl':False},
        {'name':'1.2.week','tc':pweek,'tt':[7,15,20,22],'fl':False},
        
        {'name':'1.3.circle','tc':pcircle,'tt':[1.0,2.0,5.5],'fl':True},
        {'name':'1.3.fish','tc':pfish,'tt':[1.0,10.0,500.5],'fl':True},
        {'name':'1.3.rad','tc':prad,'tt':[90.0,45.0,-180.0],'fl':True},
        {'name':'1.3.deg','tc':pdeg,'tt':[3.14,-3.14,9,-15],'fl':True},
        {'name':'1.3.hypo','tc':phypo,'tt':[[1,2],[3.5,4,4],[0, 3.3]],'fl':True},
        {'name':'1.3.plot','tc':pplot,'tt':[[100.0,20.0],[34.0,17.0]],'fl':True},
        {'name':'1.3.city','tc':pcity,'tt':[[200.0,40.0],[68.0,34.0]],'fl':True},
        
        {'name':'1.4.ruen','tc':pruen,'tt':None,'fl':False},
        {'name':'1.4.doq','tc':pdoq,'tt':None,'fl':False},
        {'name':'1.4.oneq','tc':poneq,'tt':None,'fl':False},
    ]
    
    
    #Обработка спецификаций
    for spec in test_spec:
        test_name = spec['name']
        test_list = spec['tt']
        float_out = spec['fl']
        test_obj = spec['tc'](float_out,test_list)
        tbl = test_obj.gen()
        print('#{}:\n{}\n'.format(test_name,tbl))
        
    #print('1.2.hung 456,123,980')
    #main2_hung(456)
    #main2_hung(123)
    #main2_hung(980)
    #print('1.2.rev 0')
    #main2_rev(0)
    #print('1.3.circle 1.0, 2.0, 5.5')
    #main3_circle(1.0)
    #main3_circle(2.0)
    #main3_circle(5.5)
    #print('1.3.fish 1.0, 10.0, 500.5')
    #main3_fish(1.0)
    #main3_fish(10.0)
    #main3_fish(500.5)
    #print('1.3.rad 90.0, 45.0, -180.0')
    
    
