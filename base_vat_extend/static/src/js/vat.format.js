odoo.define('vat.format', function(require)
{
    var formats = require('web.formats');
    var core = require('web.core');
    var common = require('web.form_common');
    var FieldChar = core.form_widget_registry.get('char');

    var VatFormat = FieldChar.extend({

        formatter: function(val){
            var res = "";
            var country = val.substring(0,2);
            if (country==='CL'){
                    var rut = val.substring(2,val.length -1);
                    var dv = val.substring(val.length-1, val.length);
                    rut = formats.format_value(Number(rut),{ type: 'integer'});
                    res = rut+'-'+dv;
                }
            else{
                res = val;
            }
            return res;
        },
        render_value: function() {
            console.log('render value '+ this.get('value'));
            var show_value = this.format_value(this.get('value'), '');
            if(this.get('effective_readonly')) {
                show_value = this.formatter(show_value);
            }

            if (this.$input) {
                this.$input.val(show_value);
            } else {
                if (this.password) {
                    show_value = new Array(show_value.length + 1).join('*');
                }
                this.$el.text(show_value);
            }
        },

    });


        core.form_widget_registry.add(
            'vat_format', VatFormat);
        return {
        VatFormat: VatFormat,
    }
});