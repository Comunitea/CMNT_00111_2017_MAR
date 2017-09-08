# -*- coding: utf-8 -*-


from openerp import SUPERUSER_ID
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp.exceptions import Warning

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class acp_import(osv.osv):
    _inherit = 'res.company'
        	 


    def import_asientos(self,cr,uid,ids,context=None):
         am = self.pool.get('account.move')
         alm = self.pool.get('account.move.line')         
         acc = self.pool.get('account.account')          
         ap = self.pool.get('account.period')           


         cr.execute('select * from asientos_temp ')
         res = cr.dictfetchall()
         print 'res'
         print res
         for prod in res:

             periodo = ap.search(cr,uid,[('code','=', prod['periodo'])],context=None)
             print 'periodo'
             print periodo
             vals ={
                  'ref':  prod['concepto'] ,
                  'journal_id'  : 6,
                  'period_id' : periodo[0],
                  'date' : prod['fecha']
                   }
             asiento_id = am.create(cr, uid, vals, context=context)
             #HABER7000005
             cuenta = acc.search(cr,uid,[('code','=', '7000005')],context=None)
             vals ={
                  'ref':  prod['concepto'] ,
                  'journal_id'  : 6,
                  'period_id' : periodo[0],
                  'date' : prod['fecha'],
                  'credit' :prod['haber7000005'],
                  'debit':0.0,
                  'account_id':cuenta[0],
                  'name': prod['concepto'] ,
                  'move_id': asiento_id

                   }
             alm.create(cr, uid, vals, context=context)

             #HABER4770021
             cuenta = acc.search(cr,uid,[('code','=', '4770021')],context=None)
             vals ={
                  'ref':  prod['concepto'] ,
                  'journal_id'  : 6,
                  'period_id' : periodo[0],
                  'date' : prod['fecha'],
                  'credit' :prod['haber4770021'],
                  'debit':0.0,
                  'account_id': cuenta[0],
                  'name': prod['concepto'] ,
                  'move_id': asiento_id
                   }
             alm.create(cr, uid, vals, context=context)             
             #DEBE4300011
             cuenta = acc.search(cr,uid,[('code','=', '4300011')],context=None)
             vals ={
                  'ref':  prod['concepto'] ,
                  'journal_id'  : 6,
                  'period_id' : periodo[0],
                  'date' : prod['fecha'],
                  'credit' :0.0,
                  'debit':prod['debe4300011'],
                  'account_id':cuenta[0],
                  'name': prod['concepto'] ,
                  'move_id': asiento_id
                   }
             alm.create(cr, uid, vals, context=context)              
             #DEBE4300012             
             cuenta = acc.search(cr,uid,[('code','=', '4300012')],context=None)
             vals ={
                  'ref':  prod['concepto'] ,
                  'journal_id'  : 6,
                  'period_id' : periodo[0],
                  'date' : prod['fecha'],
                  'credit' :0.0,
                  'debit':prod['debe4300012'],
                  'account_id':cuenta[0],
                  'name': prod['concepto'] ,
                  'move_id': asiento_id
                   }
             alm.create(cr, uid, vals, context=context)               
         
         #FACTORYYYYYYYYYYYYYY
         #FACTORYYYYYYYYYYYYYY
         #FACTORYYYYYYYYYYYYYY
         #FACTORYYYYYYYYYYYYYY

         cr.execute('select * from asientos_temp_factory ')
         res = cr.dictfetchall()
         print 'res'
         print res
         for prod in res:

             periodo = ap.search(cr,uid,[('code','=', prod['periodo'])],context=None)
             print 'periodo'
             print periodo
             vals ={
                  'ref':  prod['concepto'] ,
                  'journal_id'  : 6,
                  'period_id' : periodo[0],
                  'date' : prod['fecha']
                   }
             asiento_id = am.create(cr, uid, vals, context=context)
             #HABER7000003
             cuenta = acc.search(cr,uid,[('code','=', '7000003')],context=None)
             vals ={
                  'ref':  prod['concepto'] ,
                  'journal_id'  : 6,
                  'period_id' : periodo[0],
                  'date' : prod['fecha'],
                  'credit' :prod['haber7000003'],
                  'debit':0.0,
                  'account_id':cuenta[0],
                  'name': prod['concepto'] ,
                  'move_id': asiento_id

                   }
             alm.create(cr, uid, vals, context=context)

             #HABER4770021
             cuenta = acc.search(cr,uid,[('code','=', '4770021')],context=None)
             vals ={
                  'ref':  prod['concepto'] ,
                  'journal_id'  : 6,
                  'period_id' : periodo[0],
                  'date' : prod['fecha'],
                  'credit' :prod['haber4770021'],
                  'debit':0.0,
                  'account_id': cuenta[0],
                  'name': prod['concepto'] ,
                  'move_id': asiento_id
                   }
             alm.create(cr, uid, vals, context=context)             
             #DEBE4300007
             cuenta = acc.search(cr,uid,[('code','=', '4300007')],context=None)
             vals ={
                  'ref':  prod['concepto'] ,
                  'journal_id'  : 6,
                  'period_id' : periodo[0],
                  'date' : prod['fecha'],
                  'credit' :0.0,
                  'debit':prod['debe4300007'],
                  'account_id':cuenta[0],
                  'name': prod['concepto'] ,
                  'move_id': asiento_id
                   }
             alm.create(cr, uid, vals, context=context)              
             #HABER4300007             
             cuenta = acc.search(cr,uid,[('code','=', '4300007')],context=None)
             vals ={
                  'ref':  prod['concepto'] ,
                  'journal_id'  : 6,
                  'period_id' : periodo[0],
                  'date' : prod['fecha'],
                  'credit' :prod['haber4300007'],
                  'debit':0.0,
                  'account_id':cuenta[0],
                  'name': prod['concepto'] ,
                  'move_id': asiento_id
                   }
             alm.create(cr, uid, vals, context=context)               


             #DEBE4300005             
             cuenta = acc.search(cr,uid,[('code','=', '4300005')],context=None)
             vals ={
                  'ref':  prod['concepto'] ,
                  'journal_id'  : 6,
                  'period_id' : periodo[0],
                  'date' : prod['fecha'],
                  'credit' :0.0,
                  'debit':prod['debe4300005'],
                  'account_id':cuenta[0],
                  'name': prod['concepto'] ,
                  'move_id': asiento_id
                   }
             alm.create(cr, uid, vals, context=context) 

             #DEBE4300005_2            
             cuenta = acc.search(cr,uid,[('code','=', '4300005')],context=None)
             vals ={
                  'ref':  prod['concepto'] ,
                  'journal_id'  : 6,
                  'period_id' : periodo[0],
                  'date' : prod['fecha'],
                  'credit' :0.0,
                  'debit':prod['debe4300005_2'],
                  'account_id':cuenta[0],
                  'name': prod['concepto'] ,
                  'move_id': asiento_id
                   }
             alm.create(cr, uid, vals, context=context) 

             #DEBE4300006            
             cuenta = acc.search(cr,uid,[('code','=', '4300006')],context=None)
             vals ={
                  'ref':  prod['concepto'] ,
                  'journal_id'  : 6,
                  'period_id' : periodo[0],
                  'date' : prod['fecha'],
                  'credit' :0.0,
                  'debit':prod['debe4300006'],
                  'account_id':cuenta[0],
                  'name': prod['concepto'] ,
                  'move_id': asiento_id
                   }
             alm.create(cr, uid, vals, context=context) 

             #HABER4300005            
             cuenta = acc.search(cr,uid,[('code','=', '4300005')],context=None)
             vals ={
                  'ref':  prod['concepto'] ,
                  'journal_id'  : 6,
                  'period_id' : periodo[0],
                  'date' : prod['fecha'],
                  'credit' :prod['haber4300005'],
                  'debit': 0.0,
                  'account_id':cuenta[0],
                  'name': prod['concepto'] ,
                  'move_id': asiento_id
                   }
             alm.create(cr, uid, vals, context=context) 
             
             #DEBE5700000            
             cuenta = acc.search(cr,uid,[('code','=', '5700000')],context=None)
             vals ={
                  'ref':  prod['concepto'] ,
                  'journal_id'  : 6,
                  'period_id' : periodo[0],
                  'date' : prod['fecha'],
                  'credit' :0.0,
                  'debit': prod['debe5700000'],
                  'account_id':cuenta[0],
                  'name': prod['concepto'] ,
                  'move_id': asiento_id
                   }
             alm.create(cr, uid, vals, context=context) 

         #ARJONA
         #ARJONA
         #ARJONA
         #ARJONA

         cr.execute('select * from asientos_temp_arjona ')
         res = cr.dictfetchall()
         print 'res'
         print res
         for prod in res:

             periodo = ap.search(cr,uid,[('code','=', prod['periodo'])],context=None)
             print 'periodo'
             print periodo
             vals ={
                  'ref':  prod['concepto'] ,
                  'journal_id'  : 6,
                  'period_id' : periodo[0],
                  'date' : prod['fecha']
                   }
             asiento_id = am.create(cr, uid, vals, context=context)
             #HABER7000004
             cuenta = acc.search(cr,uid,[('code','=', '7000004')],context=None)
             vals ={
                  'ref':  prod['concepto'] ,
                  'journal_id'  : 6,
                  'period_id' : periodo[0],
                  'date' : prod['fecha'],
                  'credit' :prod['haber7000004'],
                  'debit':0.0,
                  'account_id':cuenta[0],
                  'name': prod['concepto'] ,
                  'move_id': asiento_id

                   }
             alm.create(cr, uid, vals, context=context)

             #HABER4770021
             cuenta = acc.search(cr,uid,[('code','=', '4770021')],context=None)
             vals ={
                  'ref':  prod['concepto'] ,
                  'journal_id'  : 6,
                  'period_id' : periodo[0],
                  'date' : prod['fecha'],
                  'credit' :prod['haber4770021'],
                  'debit':0.0,
                  'account_id': cuenta[0],
                  'name': prod['concepto'] ,
                  'move_id': asiento_id
                   }
             alm.create(cr, uid, vals, context=context)             
             #HABER4300010
             cuenta = acc.search(cr,uid,[('code','=', '4300010')],context=None)
             vals ={
                  'ref':  prod['concepto'] ,
                  'journal_id'  : 6,
                  'period_id' : periodo[0],
                  'date' : prod['fecha'],
                  'credit' :prod['haber4300010'],
                  'debit':0.0,
                  'account_id':cuenta[0],
                  'name': prod['concepto'] ,
                  'move_id': asiento_id
                   }
             alm.create(cr, uid, vals, context=context)              
             #DEBE4300010             
             cuenta = acc.search(cr,uid,[('code','=', '4300010')],context=None)
             vals ={
                  'ref':  prod['concepto'] ,
                  'journal_id'  : 6,
                  'period_id' : periodo[0],
                  'date' : prod['fecha'],
                  'credit' :0.0,
                  'debit':prod['debe4300010'],
                  'account_id':cuenta[0],
                  'name': prod['concepto'] ,
                  'move_id': asiento_id
                   }
             alm.create(cr, uid, vals, context=context)               


             #DEBE4300008             
             cuenta = acc.search(cr,uid,[('code','=', '4300008')],context=None)
             vals ={
                  'ref':  prod['concepto'] ,
                  'journal_id'  : 6,
                  'period_id' : periodo[0],
                  'date' : prod['fecha'],
                  'credit' :0.0,
                  'debit':prod['debe4300008'],
                  'account_id':cuenta[0],
                  'name': prod['concepto'] ,
                  'move_id': asiento_id
                   }
             alm.create(cr, uid, vals, context=context) 

             #DEBE4300008_2            
             cuenta = acc.search(cr,uid,[('code','=', '4300008')],context=None)
             vals ={
                  'ref':  prod['concepto'] ,
                  'journal_id'  : 6,
                  'period_id' : periodo[0],
                  'date' : prod['fecha'],
                  'credit' :0.0,
                  'debit':prod['debe4300008_2'],
                  'account_id':cuenta[0],
                  'name': prod['concepto'] ,
                  'move_id': asiento_id
                   }
             alm.create(cr, uid, vals, context=context) 

             #DEBE4300009            
             cuenta = acc.search(cr,uid,[('code','=', '4300009')],context=None)
             vals ={
                  'ref':  prod['concepto'] ,
                  'journal_id'  : 6,
                  'period_id' : periodo[0],
                  'date' : prod['fecha'],
                  'credit' :0.0,
                  'debit':prod['debe4300009'],
                  'account_id':cuenta[0],
                  'name': prod['concepto'] ,
                  'move_id': asiento_id
                   }
             alm.create(cr, uid, vals, context=context) 
            
             #HABER4300008            
             cuenta = acc.search(cr,uid,[('code','=', '4300008')],context=None)
             vals ={
                  'ref':  prod['concepto'] ,
                  'journal_id'  : 6,
                  'period_id' : periodo[0],
                  'date' : prod['fecha'],
                  'credit' :prod['haber4300008'],
                  'debit': 0.0,
                  'account_id':cuenta[0],
                  'name': prod['concepto'] ,
                  'move_id': asiento_id
                   }
             alm.create(cr, uid, vals, context=context)             
             #DEBE5700000            
             cuenta = acc.search(cr,uid,[('code','=', '5700000')],context=None)
             vals ={
                  'ref':  prod['concepto'] ,
                  'journal_id'  : 6,
                  'period_id' : periodo[0],
                  'date' : prod['fecha'],
                  'credit' :0.0,
                  'debit':prod['debe5700000'],
                  'account_id':cuenta[0],
                  'name': prod['concepto'] ,
                  'move_id': asiento_id
                   }
             alm.create(cr, uid, vals, context=context) 
         #VISO
         #VISO
         #VISO
         #VISO

         cr.execute('select * from asientos_temp_viso ')
         res = cr.dictfetchall()
         print 'res'
         print res
         for prod in res:

             periodo = ap.search(cr,uid,[('code','=', prod['periodo'])],context=None)
             print 'periodo'
             print periodo
             vals ={
                  'ref':  prod['concepto'] ,
                  'journal_id'  : 6,
                  'period_id' : periodo[0],
                  'date' : prod['fecha']
                   }
             asiento_id = am.create(cr, uid, vals, context=context)
             #HABER7000002
             cuenta = acc.search(cr,uid,[('code','=', '7000002')],context=None)
             vals ={
                  'ref':  prod['concepto'] ,
                  'journal_id'  : 6,
                  'period_id' : periodo[0],
                  'date' : prod['fecha'],
                  'credit' :prod['haber7000002'],
                  'debit':0.0,
                  'account_id':cuenta[0],
                  'name': prod['concepto'] ,
                  'move_id': asiento_id

                   }
             alm.create(cr, uid, vals, context=context)

             #HABER4770021
             cuenta = acc.search(cr,uid,[('code','=', '4770021')],context=None)
             vals ={
                  'ref':  prod['concepto'] ,
                  'journal_id'  : 6,
                  'period_id' : periodo[0],
                  'date' : prod['fecha'],
                  'credit' :prod['haber4770021'],
                  'debit':0.0,
                  'account_id': cuenta[0],
                  'name': prod['concepto'] ,
                  'move_id': asiento_id
                   }
             alm.create(cr, uid, vals, context=context)             
             #DEBE4300004
             cuenta = acc.search(cr,uid,[('code','=', '4300004')],context=None)
             vals ={
                  'ref':  prod['concepto'] ,
                  'journal_id'  : 6,
                  'period_id' : periodo[0],
                  'date' : prod['fecha'],
                  'credit' :0.0,
                  'debit':prod['debe4300004'],
                  'account_id':cuenta[0],
                  'name': prod['concepto'] ,
                  'move_id': asiento_id
                   }
             alm.create(cr, uid, vals, context=context)              
             #HABER4300004             
             cuenta = acc.search(cr,uid,[('code','=', '4300004')],context=None)
             vals ={
                  'ref':  prod['concepto'] ,
                  'journal_id'  : 6,
                  'period_id' : periodo[0],
                  'date' : prod['fecha'],
                  'credit' :prod['haber4300004'],
                  'debit': 0.0,
                  'account_id':cuenta[0],
                  'name': prod['concepto'] ,
                  'move_id': asiento_id
                   }
             alm.create(cr, uid, vals, context=context)               


             #DEBE4300002             
             cuenta = acc.search(cr,uid,[('code','=', '4300002')],context=None)
             vals ={
                  'ref':  prod['concepto'] ,
                  'journal_id'  : 6,
                  'period_id' : periodo[0],
                  'date' : prod['fecha'],
                  'credit' :0.0,
                  'debit':prod['debe4300002'],
                  'account_id':cuenta[0],
                  'name': prod['concepto'] ,
                  'move_id': asiento_id
                   }
             alm.create(cr, uid, vals, context=context) 

             #DEBE4300002_2            
             cuenta = acc.search(cr,uid,[('code','=', '4300002')],context=None)
             vals ={
                  'ref':  prod['concepto'] ,
                  'journal_id'  : 6,
                  'period_id' : periodo[0],
                  'date' : prod['fecha'],
                  'credit' :0.0,
                  'debit':prod['debe4300002_2'],
                  'account_id':cuenta[0],
                  'name': prod['concepto'] ,
                  'move_id': asiento_id
                   }
             alm.create(cr, uid, vals, context=context) 

             #DEBE4300003            
             cuenta = acc.search(cr,uid,[('code','=', '4300003')],context=None)
             vals ={
                  'ref':  prod['concepto'] ,
                  'journal_id'  : 6,
                  'period_id' : periodo[0],
                  'date' : prod['fecha'],
                  'credit' :0.0,
                  'debit':prod['debe4300003'],
                  'account_id':cuenta[0],
                  'name': prod['concepto'] ,
                  'move_id': asiento_id
                   }
             alm.create(cr, uid, vals, context=context)          
 
         #PAGO
         #PAGO
         #PAGO
 




         cr.execute('select * from asientos_temp_tocina')
         res = cr.dictfetchall()
         print 'res'
         print res
         for prod in res:

             periodo = ap.search(cr,uid,[('code','=', prod['periodo'])],context=None)
             print 'periodo'
             print periodo
             vals ={
                  'ref':  prod['concepto'] ,
                  'journal_id'  : 6,
                  'period_id' : periodo[0],
                  'date' : prod['fecha']
                   }
             asiento_id = am.create(cr, uid, vals, context=context)
             #HABER - 7000005
             cuenta = acc.search(cr,uid,[('code','=', '7000005')],context=None)
             vals ={
                  'ref':  prod['concepto'] ,
                  'journal_id'  : 6,
                  'period_id' : periodo[0],
                  'date' : prod['fecha'],
                  'credit' :prod['haber7000005'],
                  'debit':0.0,
                  'account_id':cuenta[0],
                  'name': prod['concepto'] ,
                  'move_id': asiento_id

                   }
             alm.create(cr, uid, vals, context=context)

             #HABER4770021
             cuenta = acc.search(cr,uid,[('code','=', '4770021')],context=None)
             vals ={
                  'ref':  prod['concepto'] ,
                  'journal_id'  : 6,
                  'period_id' : periodo[0],
                  'date' : prod['fecha'],
                  'credit' :prod['haber4770021'],
                  'debit':0.0,
                  'account_id': cuenta[0],
                  'name': prod['concepto'] ,
                  'move_id': asiento_id
                   }
             alm.create(cr, uid, vals, context=context)             
             #DEBE - 4300011
             cuenta = acc.search(cr,uid,[('code','=', '4300011')],context=None)
             vals ={
                  'ref':  prod['concepto'] ,
                  'journal_id'  : 6,
                  'period_id' : periodo[0],
                  'date' : prod['fecha'],
                  'credit' :0.0,
                  'debit':prod['debe4300011'],
                  'account_id':cuenta[0],
                  'name': prod['concepto'] ,
                  'move_id': asiento_id
                   }
             alm.create(cr, uid, vals, context=context)              
             #DEBE - 4300012             
             cuenta = acc.search(cr,uid,[('code','=', '4300012')],context=None)
             vals ={
                  'ref':  prod['concepto'] ,
                  'journal_id'  : 6,
                  'period_id' : periodo[0],
                  'date' : prod['fecha'],
                  'credit' :0.0,
                  'debit':prod['debe4300012'],
                  'account_id':cuenta[0],
                  'name': prod['concepto'] ,
                  'move_id': asiento_id
                   }
             alm.create(cr, uid, vals, context=context)               




             #HABER-4300011
           
             cuenta = acc.search(cr,uid,[('code','=', '4300011')],context=None)
             vals ={
                  'ref':  prod['concepto'] ,
                  'journal_id'  : 6,
                  'period_id' : periodo[0],
                  'date' : prod['fecha'],
                  'credit' :prod['haber4300011'],
                  'debit': 0.0,
                  'account_id':cuenta[0],
                  'name': prod['concepto'] ,
                  'move_id': asiento_id
                   }
             alm.create(cr, uid, vals, context=context) 
             
             #DEBE5700000            
             cuenta = acc.search(cr,uid,[('code','=', '5700000')],context=None)
             vals ={
                  'ref':  prod['concepto'] ,
                  'journal_id'  : 6,
                  'period_id' : periodo[0],
                  'date' : prod['fecha'],
                  'credit' :0.0,
                  'debit': prod['debe5700000'],
                  'account_id':cuenta[0],
                  'name': prod['concepto'] ,
                  'move_id': asiento_id
                   }
             alm.create(cr, uid, vals, context=context) 


acp_import()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
