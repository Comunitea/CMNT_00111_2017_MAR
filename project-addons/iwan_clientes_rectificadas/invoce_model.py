from openerp import api, fields, models

class AccountInvoceExt(models.Model):
    _inherit = "account.invoice"

    rect_residual = fields.Float(string='Saldo pendiente', compute='_compute_residual_signo_rectificativa')
    @api.one
    @api.depends('residual','type')
    def _compute_residual_signo_rectificativa(self):
       if self.type == 'out_refund':
          self.rect_residual = self.residual * -1
       else:
           self.rect_residual = self.residual


    rect_amount_untaxed = fields.Float(string='Subtotal', compute='_compute_untaxed_signo_rectificativa')
    @api.one
    @api.depends('amount_untaxed','type')
    def _compute_untaxed_signo_rectificativa(self):
       if self.type == 'out_refund' or  self.type == 'in_refund':
          self.rect_amount_untaxed = self.amount_untaxed * -1
       else:
           self.rect_amount_untaxed = self.amount_untaxed


    rect_amount_total = fields.Float(string='Total', compute='_compute_total_signo_rectificativa')
    @api.one
    @api.depends('amount_total','type')
    def _compute_total_signo_rectificativa(self):
       if self.type == 'out_refund' or self.type == 'in_refund':
          self.rect_amount_total = round(self.amount_total * -1,2)
       else:
          self.rect_amount_total = round(self.amount_total,2)



