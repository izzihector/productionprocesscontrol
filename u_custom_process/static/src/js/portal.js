odoo.define('u_custom_process.portal', function(require) {
    'use strict';

    var publicWidget = require('web.public.widget');

    publicWidget.registry.processSearchPanel = publicWidget.Widget.extend({
        selector: '.o_portal_search_panel_dates',
        events: {
            'click .search-submit': '_onSearchSubmitClick',
            'keyup input[name="date_begin"]': '_onSearchInputKeyup',
            'keyup input[name="date_end"]': '_onSearchInputKeyup',
        },

        /**
         * @override
         */
        start: function() {
            var def = this._super.apply(this, arguments);
            return def;
        },

        //--------------------------------------------------------------------------
        // Private
        //--------------------------------------------------------------------------

        /**
         * @private
         */
        _search: function() {
            var search = $.deparam(window.location.search.substring(1));
            search['date_begin'] = this.$('input[name="date_begin"]').val();
            search['date_end'] = this.$('input[name="date_end"]').val();
            window.location.search = $.param(search);
        },

        //--------------------------------------------------------------------------
        // Handlers
        //--------------------------------------------------------------------------

        /**
         * @private
         */
        _onSearchSubmitClick: function() {
            this._search();
        },
        /**
         * @private
         */
        _onSearchInputKeyup: function(ev) {
            if (ev.keyCode === $.ui.keyCode.ENTER) {
                this._search();
            }
        },
    });

});