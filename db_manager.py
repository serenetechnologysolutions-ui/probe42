import mysql.connector


class DatabaseManager:
    DB_NAME = "probe42_data"

    def __init__(self, host="127.0.0.1", port=3306, user="root", password="Root@123"):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.connection = None

    def _get_connection(self, database=None):
        config = {
            "host": self.host,
            "port": self.port,
            "user": self.user,
            "password": self.password,
        }
        if database:
            config["database"] = database
        return mysql.connector.connect(**config)

    def initialize(self):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.DB_NAME}")
        cursor.close()
        conn.close()

        self.connection = self._get_connection(database=self.DB_NAME)
        cursor = self.connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS companies (
                id INT AUTO_INCREMENT PRIMARY KEY,
                cin VARCHAR(21) UNIQUE NOT NULL,
                legal_name VARCHAR(255) NOT NULL,
                pan VARCHAR(10),
                efiling_status VARCHAR(50),
                incorporation_date VARCHAR(20),
                paid_up_capital BIGINT,
                authorized_capital BIGINT,
                active_compliance VARCHAR(50),
                classification VARCHAR(255),
                status VARCHAR(50),
                website VARCHAR(255),
                email VARCHAR(255),
                registered_address TEXT,
                business_address TEXT,
                last_agm_date VARCHAR(20),
                last_filing_date VARCHAR(20),
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS directors (
                id INT AUTO_INCREMENT PRIMARY KEY,
                cin VARCHAR(21) NOT NULL,
                pan VARCHAR(10),
                din VARCHAR(20),
                name VARCHAR(255),
                designation VARCHAR(100),
                din_status VARCHAR(50),
                gender VARCHAR(20),
                date_of_birth VARCHAR(20),
                date_of_appointment VARCHAR(20),
                date_of_cessation VARCHAR(20),
                nationality VARCHAR(50),
                address TEXT,
                INDEX idx_cin (cin)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS financials (
                id INT AUTO_INCREMENT PRIMARY KEY,
                cin VARCHAR(21) NOT NULL,
                year VARCHAR(20),
                nature VARCHAR(50),
                filing_type VARCHAR(50),
                filing_standard VARCHAR(50),
                INDEX idx_cin (cin)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS financial_ratios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                cin VARCHAR(21) NOT NULL,
                year VARCHAR(20),
                revenue_growth DOUBLE,
                gross_profit_margin DOUBLE,
                net_margin DOUBLE,
                ebitda_margin DOUBLE,
                return_on_equity DOUBLE,
                return_on_capital_employed DOUBLE,
                debt_ratio DOUBLE,
                debt_by_equity DOUBLE,
                interest_coverage_ratio DOUBLE,
                current_ratio DOUBLE,
                quick_ratio DOUBLE,
                inventory_by_sales_days DOUBLE,
                debtors_by_sales_days DOUBLE,
                payables_by_sales_days DOUBLE,
                cash_conversion_cycle DOUBLE,
                sales_by_net_fixed_assets DOUBLE,
                INDEX idx_cin (cin)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS financial_balance_sheet (
                id INT AUTO_INCREMENT PRIMARY KEY,
                cin VARCHAR(21) NOT NULL,
                year VARCHAR(20),
                tangible_assets BIGINT,
                intangible_assets BIGINT,
                tangible_assets_capital_work_in_progress BIGINT,
                noncurrent_investments BIGINT,
                deferred_tax_assets_net BIGINT,
                long_term_loans_and_advances BIGINT,
                other_noncurrent_assets BIGINT,
                current_investments BIGINT,
                inventories BIGINT,
                trade_receivables BIGINT,
                cash_and_bank_balances BIGINT,
                short_term_loans_and_advances BIGINT,
                other_current_assets BIGINT,
                given_assets_total BIGINT,
                share_capital BIGINT,
                reserves_and_surplus BIGINT,
                minority_interest BIGINT,
                long_term_borrowings BIGINT,
                deferred_tax_liabilities_net BIGINT,
                other_long_term_liabilities BIGINT,
                long_term_provisions BIGINT,
                short_term_borrowings BIGINT,
                trade_payables BIGINT,
                other_current_liabilities BIGINT,
                short_term_provisions BIGINT,
                given_liabilities_total BIGINT,
                total_equity BIGINT,
                total_non_current_liabilities BIGINT,
                total_current_liabilities BIGINT,
                net_fixed_assets BIGINT,
                total_current_assets BIGINT,
                total_debt BIGINT,
                INDEX idx_cin (cin)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS financial_pnl (
                id INT AUTO_INCREMENT PRIMARY KEY,
                cin VARCHAR(21) NOT NULL,
                year VARCHAR(20),
                net_revenue BIGINT,
                total_cost_of_materials_consumed BIGINT,
                total_purchases_of_stock_in_trade BIGINT,
                total_changes_in_inventories BIGINT,
                total_employee_benefit_expense BIGINT,
                total_other_expenses BIGINT,
                operating_profit BIGINT,
                other_income BIGINT,
                depreciation BIGINT,
                profit_before_interest_and_tax BIGINT,
                interest BIGINT,
                profit_before_tax BIGINT,
                income_tax BIGINT,
                profit_after_tax BIGINT,
                total_operating_cost BIGINT,
                INDEX idx_cin (cin)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS financial_cash_flow (
                id INT AUTO_INCREMENT PRIMARY KEY,
                cin VARCHAR(21) NOT NULL,
                year VARCHAR(20),
                profit_before_tax BIGINT,
                adjustment_for_finance_cost_and_depreciation BIGINT,
                adjustment_for_current_and_non_current_assets BIGINT,
                adjustment_for_current_and_non_current_liabilities BIGINT,
                other_adjustments_in_operating_activities BIGINT,
                cash_flows_from_used_in_operating_activities BIGINT,
                cash_outflow_from_purchase_of_assets BIGINT,
                cash_inflow_from_sale_of_assets BIGINT,
                income_from_assets BIGINT,
                other_adjustments_in_investing_activities BIGINT,
                cash_flows_from_used_in_investing_activities BIGINT,
                cash_outflow_from_repayment_of_capital_and_borrowings BIGINT,
                cash_inflow_from_raisng_capital_and_borrowings BIGINT,
                interest_and_dividends_paid BIGINT,
                other_adjustments_in_financing_activities BIGINT,
                cash_flows_from_used_in_financing_activities BIGINT,
                incr_decr_in_cash_cash_equv BIGINT,
                cash_flow_statement_at_end_of_period BIGINT,
                INDEX idx_cin (cin)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS financial_pnl_key_schedule (
                id INT AUTO_INCREMENT PRIMARY KEY,
                cin VARCHAR(21) NOT NULL,
                year VARCHAR(20),
                managerial_remuneration BIGINT,
                payment_to_auditors BIGINT,
                insurance_expenses BIGINT,
                power_and_fuel BIGINT,
                INDEX idx_cin (cin)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS financial_auditor (
                id INT AUTO_INCREMENT PRIMARY KEY,
                cin VARCHAR(21) NOT NULL,
                year VARCHAR(20),
                auditor_name VARCHAR(255),
                auditor_firm_name VARCHAR(255),
                pan VARCHAR(20),
                membership_number VARCHAR(20),
                firm_registration_number VARCHAR(50),
                address TEXT,
                report_has_adverse_remarks BOOLEAN,
                INDEX idx_cin (cin)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS financial_revenue_breakup (
                id INT AUTO_INCREMENT PRIMARY KEY,
                cin VARCHAR(21) NOT NULL,
                year VARCHAR(20),
                revenue_from_operations BIGINT,
                revenue_from_interest BIGINT,
                revenue_from_other_financial_services BIGINT,
                revenue_from_sale_of_products BIGINT,
                revenue_from_sale_of_services BIGINT,
                other_operating_revenues BIGINT,
                excise_duty BIGINT,
                depreciation BIGINT,
                amortisation BIGINT,
                INDEX idx_cin (cin)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS financial_parameters (
                id INT AUTO_INCREMENT PRIMARY KEY,
                cin VARCHAR(21) NOT NULL,
                year VARCHAR(20),
                nature VARCHAR(50),
                earning_fc BIGINT,
                expenditure_fc BIGINT,
                transaction_related_parties_as_18 BIGINT,
                employee_benefit_expense BIGINT,
                number_of_employees INT,
                prescribed_csr_expenditure DOUBLE,
                total_amount_csr_spent_for_financial_year BIGINT,
                gross_fixed_assets BIGINT,
                trade_receivable_exceeding_six_months BIGINT,
                proposed_dividend VARCHAR(100),
                INDEX idx_cin (cin)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS shareholdings (
                id INT AUTO_INCREMENT PRIMARY KEY,
                cin VARCHAR(21) NOT NULL,
                year VARCHAR(20),
                financial_year VARCHAR(20),
                category VARCHAR(100),
                total_no_of_shares BIGINT,
                promoter_shares BIGINT,
                public_shares BIGINT,
                INDEX idx_cin (cin)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS gst_details (
                id INT AUTO_INCREMENT PRIMARY KEY,
                cin VARCHAR(21) NOT NULL,
                gstin VARCHAR(20),
                status VARCHAR(50),
                company_name VARCHAR(255),
                trade_name VARCHAR(255),
                state VARCHAR(100),
                date_of_registration VARCHAR(20),
                taxpayer_type VARCHAR(100),
                INDEX idx_cin (cin)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS legal_history (
                id INT AUTO_INCREMENT PRIMARY KEY,
                cin VARCHAR(21) NOT NULL,
                petitioner TEXT,
                respondent TEXT,
                court VARCHAR(255),
                date VARCHAR(20),
                case_status VARCHAR(50),
                case_number VARCHAR(100),
                case_type VARCHAR(100),
                case_category VARCHAR(100),
                severity VARCHAR(50),
                INDEX idx_cin (cin)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS charges (
                id INT AUTO_INCREMENT PRIMARY KEY,
                cin VARCHAR(21) NOT NULL,
                charge_id VARCHAR(50),
                charge_holder VARCHAR(255),
                date_of_creation VARCHAR(20),
                date_of_modification VARCHAR(20),
                amount BIGINT,
                status VARCHAR(50),
                INDEX idx_cin (cin)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS contact_details (
                id INT AUTO_INCREMENT PRIMARY KEY,
                cin VARCHAR(21) NOT NULL,
                emails TEXT,
                phones TEXT,
                INDEX idx_cin (cin)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS epfo_establishments (
                id INT AUTO_INCREMENT PRIMARY KEY,
                cin VARCHAR(21) NOT NULL,
                establishment_id VARCHAR(50),
                establishment_name VARCHAR(255),
                working_status VARCHAR(50),
                date_of_setup VARCHAR(20),
                address TEXT,
                no_of_employees INT,
                INDEX idx_cin (cin)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS credit_ratings (
                id INT AUTO_INCREMENT PRIMARY KEY,
                cin VARCHAR(21) NOT NULL,
                agency VARCHAR(100),
                instrument VARCHAR(255),
                rating VARCHAR(50),
                rating_date VARCHAR(20),
                INDEX idx_cin (cin)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS related_party_transactions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                cin VARCHAR(21) NOT NULL,
                financial_year VARCHAR(20),
                party_name VARCHAR(255),
                party_type VARCHAR(50),
                relationship VARCHAR(255),
                transaction_details TEXT,
                INDEX idx_cin (cin)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS data_status (
                id INT AUTO_INCREMENT PRIMARY KEY,
                cin VARCHAR(21) UNIQUE NOT NULL,
                efiling_status VARCHAR(50),
                next_cin VARCHAR(21),
                last_base_updated VARCHAR(20),
                last_details_updated VARCHAR(20),
                last_fin_year_end VARCHAR(20),
                last_filing_date VARCHAR(20),
                last_annual_returns_year_end VARCHAR(20),
                last_epfo_updated VARCHAR(20),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS error_logs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                error_code INT NOT NULL,
                error_message VARCHAR(255) NOT NULL,
                cin_queried VARCHAR(21) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        self.connection.commit()
        cursor.close()

    def store_full_response(self, cin, data):
        """Store the full API response across all tables."""
        company = data.get("data", {}).get("company", {})
        self._store_company(cin, company, data.get("data", {}))
        self._store_directors(cin, data.get("data", {}).get("authorized_signatories", []))
        self._store_financials(cin, data.get("data", {}).get("financials", []))
        self._store_financial_parameters(cin, data.get("data", {}).get("financial_parameters", []))
        self._store_shareholdings(cin, data.get("data", {}).get("shareholdings", []))
        self._store_gst(cin, data.get("data", {}).get("gst_details", []))
        self._store_legal(cin, data.get("data", {}).get("legal_history", []))
        self._store_charges(cin, data.get("data", {}).get("open_charges", []))
        self._store_contacts(cin, data.get("data", {}).get("contact_details", {}))
        self._store_epfo(cin, data.get("data", {}).get("establishments_registered_with_epfo", []))
        self._store_credit_ratings(cin, data.get("data", {}).get("credit_ratings", []))
        self._store_rpt(cin, data.get("data", {}).get("related_party_transactions", []))

    def _store_company(self, cin, company, full_data):
        desc = full_data.get("description", {}).get("desc_thousand_char", "")
        reg_addr = company.get("registered_address", {})
        reg_addr_str = reg_addr.get("full_address", "") if isinstance(reg_addr, dict) else ""
        biz_addr = company.get("business_address", {})
        biz_addr_str = ", ".join(filter(None, [
            biz_addr.get("address_line1", ""),
            biz_addr.get("address_line2", ""),
            biz_addr.get("city", ""),
            biz_addr.get("state", ""),
            str(biz_addr.get("pincode", ""))
        ])) if isinstance(biz_addr, dict) else ""

        cursor = self.connection.cursor()
        cursor.execute("""
            INSERT INTO companies (cin, legal_name, pan, efiling_status, incorporation_date,
                paid_up_capital, authorized_capital, active_compliance, classification,
                status, website, email, registered_address, business_address,
                last_agm_date, last_filing_date, description)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ON DUPLICATE KEY UPDATE
                legal_name=VALUES(legal_name), pan=VALUES(pan), efiling_status=VALUES(efiling_status),
                incorporation_date=VALUES(incorporation_date), paid_up_capital=VALUES(paid_up_capital),
                authorized_capital=VALUES(authorized_capital), active_compliance=VALUES(active_compliance),
                classification=VALUES(classification), status=VALUES(status), website=VALUES(website),
                email=VALUES(email), registered_address=VALUES(registered_address),
                business_address=VALUES(business_address), last_agm_date=VALUES(last_agm_date),
                last_filing_date=VALUES(last_filing_date), description=VALUES(description)
        """, (
            cin, company.get("legal_name", ""), company.get("pan", ""),
            company.get("efiling_status", ""), company.get("incorporation_date", ""),
            company.get("paid_up_capital"), company.get("authorized_capital"),
            company.get("active_compliance", ""), company.get("classification", ""),
            company.get("status", ""), company.get("website", ""), company.get("email", ""),
            reg_addr_str, biz_addr_str,
            company.get("last_agm_date", ""), company.get("last_filing_date", ""), desc
        ))
        self.connection.commit()
        cursor.close()

    def _store_directors(self, cin, directors):
        if not directors:
            return
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM directors WHERE cin = %s", (cin,))
        for d in directors:
            addr = d.get("address", {})
            addr_str = addr.get("full_address", ", ".join(filter(None, [
                addr.get("address_line1", ""), addr.get("city", ""), addr.get("state", "")
            ]))) if isinstance(addr, dict) else ""
            cursor.execute("""
                INSERT INTO directors (cin, pan, din, name, designation, din_status,
                    gender, date_of_birth, date_of_appointment, date_of_cessation, nationality, address)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, (cin, d.get("pan", ""), d.get("din", ""), d.get("name", ""),
                  d.get("designation", ""), d.get("din_status", ""), d.get("gender", ""),
                  d.get("date_of_birth", ""), d.get("date_of_appointment", ""),
                  d.get("date_of_cessation", ""), d.get("nationality", ""), addr_str))
        self.connection.commit()
        cursor.close()

    def _store_financials(self, cin, financials):
        if not financials:
            return
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM financials WHERE cin = %s", (cin,))
        cursor.execute("DELETE FROM financial_ratios WHERE cin = %s", (cin,))
        cursor.execute("DELETE FROM financial_balance_sheet WHERE cin = %s", (cin,))
        cursor.execute("DELETE FROM financial_pnl WHERE cin = %s", (cin,))
        cursor.execute("DELETE FROM financial_cash_flow WHERE cin = %s", (cin,))
        cursor.execute("DELETE FROM financial_pnl_key_schedule WHERE cin = %s", (cin,))
        cursor.execute("DELETE FROM financial_auditor WHERE cin = %s", (cin,))
        cursor.execute("DELETE FROM financial_revenue_breakup WHERE cin = %s", (cin,))

        for f in financials:
            year = f.get("year", "")

            # Main financials record
            cursor.execute("""
                INSERT INTO financials (cin, year, nature, filing_type, filing_standard)
                VALUES (%s,%s,%s,%s,%s)
            """, (cin, year, f.get("nature", ""), f.get("filing_type", ""), f.get("filing_standard", "")))

            # Ratios
            ratios = f.get("ratios") or {}
            if ratios:
                cursor.execute("""
                    INSERT INTO financial_ratios (cin, year, revenue_growth, gross_profit_margin,
                        net_margin, ebitda_margin, return_on_equity, return_on_capital_employed,
                        debt_ratio, debt_by_equity, interest_coverage_ratio, current_ratio,
                        quick_ratio, inventory_by_sales_days, debtors_by_sales_days,
                        payables_by_sales_days, cash_conversion_cycle, sales_by_net_fixed_assets)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """, (cin, year, ratios.get("revenue_growth"), ratios.get("gross_profit_margin"),
                      ratios.get("net_margin"), ratios.get("ebitda_margin"),
                      ratios.get("return_on_equity"), ratios.get("return_on_capital_employed"),
                      ratios.get("debt_ratio"), ratios.get("debt_by_equity"),
                      ratios.get("interest_coverage_ratio"), ratios.get("current_ratio"),
                      ratios.get("quick_ratio"), ratios.get("inventory_by_sales_days"),
                      ratios.get("debtors_by_sales_days"), ratios.get("payables_by_sales_days"),
                      ratios.get("cash_conversion_cycle"), ratios.get("sales_by_net_fixed_assets")))

            # Balance Sheet
            bs = f.get("bs") or {}
            if bs:
                assets = bs.get("assets") or {}
                liabilities = bs.get("liabilities") or {}
                sub = bs.get("subTotals") or {}
                cursor.execute("""
                    INSERT INTO financial_balance_sheet (cin, year, tangible_assets, intangible_assets,
                        tangible_assets_capital_work_in_progress, noncurrent_investments,
                        deferred_tax_assets_net, long_term_loans_and_advances, other_noncurrent_assets,
                        current_investments, inventories, trade_receivables, cash_and_bank_balances,
                        short_term_loans_and_advances, other_current_assets, given_assets_total,
                        share_capital, reserves_and_surplus, minority_interest, long_term_borrowings,
                        deferred_tax_liabilities_net, other_long_term_liabilities, long_term_provisions,
                        short_term_borrowings, trade_payables, other_current_liabilities,
                        short_term_provisions, given_liabilities_total, total_equity,
                        total_non_current_liabilities, total_current_liabilities, net_fixed_assets,
                        total_current_assets, total_debt)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """, (cin, year,
                      assets.get("tangible_assets"), assets.get("intangible_assets"),
                      assets.get("tangible_assets_capital_work_in_progress"),
                      assets.get("noncurrent_investments"), assets.get("deferred_tax_assets_net"),
                      assets.get("long_term_loans_and_advances"), assets.get("other_noncurrent_assets"),
                      assets.get("current_investments"), assets.get("inventories"),
                      assets.get("trade_receivables"), assets.get("cash_and_bank_balances"),
                      assets.get("short_term_loans_and_advances"), assets.get("other_current_assets"),
                      assets.get("given_assets_total"),
                      liabilities.get("share_capital"), liabilities.get("reserves_and_surplus"),
                      liabilities.get("minority_interest"), liabilities.get("long_term_borrowings"),
                      liabilities.get("deferred_tax_liabilities_net"),
                      liabilities.get("other_long_term_liabilities"), liabilities.get("long_term_provisions"),
                      liabilities.get("short_term_borrowings"), liabilities.get("trade_payables"),
                      liabilities.get("other_current_liabilities"), liabilities.get("short_term_provisions"),
                      liabilities.get("given_liabilities_total"),
                      sub.get("total_equity"), sub.get("total_non_current_liabilities"),
                      sub.get("total_current_liabilities"), sub.get("net_fixed_assets"),
                      sub.get("total_current_assets"), sub.get("total_debt")))

            # Profit & Loss
            pnl = f.get("pnl") or {}
            if pnl:
                items = pnl.get("lineItems") or {}
                pnl_sub = pnl.get("subTotals") or {}
                cursor.execute("""
                    INSERT INTO financial_pnl (cin, year, net_revenue, total_cost_of_materials_consumed,
                        total_purchases_of_stock_in_trade, total_changes_in_inventories,
                        total_employee_benefit_expense, total_other_expenses, operating_profit,
                        other_income, depreciation, profit_before_interest_and_tax, interest,
                        profit_before_tax, income_tax, profit_after_tax, total_operating_cost)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """, (cin, year, items.get("net_revenue"),
                      items.get("total_cost_of_materials_consumed"),
                      items.get("total_purchases_of_stock_in_trade"),
                      items.get("total_changes_in_inventories_or_finished_goods"),
                      items.get("total_employee_benefit_expense"), items.get("total_other_expenses"),
                      items.get("operating_profit"), items.get("other_income"),
                      items.get("depreciation"), items.get("profit_before_interest_and_tax"),
                      items.get("interest"), items.get("profit_before_tax"),
                      items.get("income_tax"), items.get("profit_after_tax"),
                      pnl_sub.get("total_operating_cost")))

            # Cash Flow
            cf = f.get("cash_flow") or {}
            if cf:
                cursor.execute("""
                    INSERT INTO financial_cash_flow (cin, year, profit_before_tax,
                        adjustment_for_finance_cost_and_depreciation,
                        adjustment_for_current_and_non_current_assets,
                        adjustment_for_current_and_non_current_liabilities,
                        other_adjustments_in_operating_activities,
                        cash_flows_from_used_in_operating_activities,
                        cash_outflow_from_purchase_of_assets, cash_inflow_from_sale_of_assets,
                        income_from_assets, other_adjustments_in_investing_activities,
                        cash_flows_from_used_in_investing_activities,
                        cash_outflow_from_repayment_of_capital_and_borrowings,
                        cash_inflow_from_raisng_capital_and_borrowings,
                        interest_and_dividends_paid, other_adjustments_in_financing_activities,
                        cash_flows_from_used_in_financing_activities,
                        incr_decr_in_cash_cash_equv, cash_flow_statement_at_end_of_period)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """, (cin, year, cf.get("profit_before_tax"),
                      cf.get("adjustment_for_finance_cost_and_depreciation"),
                      cf.get("adjustment_for_current_and_non_current_assets"),
                      cf.get("adjustment_for_current_and_non_current_liabilities"),
                      cf.get("other_adjustments_in_operating_activities"),
                      cf.get("cash_flows_from_used_in_operating_activities"),
                      cf.get("cash_outflow_from_purchase_of_assets"),
                      cf.get("cash_inflow_from_sale_of_assets"),
                      cf.get("income_from_assets"),
                      cf.get("other_adjustments_in_investing_activities"),
                      cf.get("cash_flows_from_used_in_investing_activities"),
                      cf.get("cash_outflow_from_repayment_of_capital_and_borrowings"),
                      cf.get("cash_inflow_from_raisng_capital_and_borrowings"),
                      cf.get("interest_and_dividends_paid"),
                      cf.get("other_adjustments_in_financing_activities"),
                      cf.get("cash_flows_from_used_in_financing_activities"),
                      cf.get("incr_decr_in_cash_cash_equv"),
                      cf.get("cash_flow_statement_at_end_of_period")))

            # PNL Key Schedule
            pnl_ks = f.get("pnl_key_schedule") or {}
            if pnl_ks:
                cursor.execute("""
                    INSERT INTO financial_pnl_key_schedule (cin, year, managerial_remuneration,
                        payment_to_auditors, insurance_expenses, power_and_fuel)
                    VALUES (%s,%s,%s,%s,%s,%s)
                """, (cin, year, pnl_ks.get("managerial_remuneration"),
                      pnl_ks.get("payment_to_auditors"), pnl_ks.get("insurance_expenses"),
                      pnl_ks.get("power_and_fuel")))

            # Auditor
            auditor = f.get("auditor") or {}
            if auditor:
                comments = f.get("auditor_comments") or {}
                cursor.execute("""
                    INSERT INTO financial_auditor (cin, year, auditor_name, auditor_firm_name,
                        pan, membership_number, firm_registration_number, address, report_has_adverse_remarks)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """, (cin, year, auditor.get("auditor_name", ""), auditor.get("auditor_firm_name", ""),
                      auditor.get("pan", ""), auditor.get("membership_number", ""),
                      auditor.get("firm_registration_number", ""), auditor.get("address", ""),
                      comments.get("report_has_adverse_remarks", False)))

            # Revenue Breakup & Depreciation Breakup
            pnl_data = f.get("pnl") or {}
            rev_breakup = pnl_data.get("revenue_breakup") or {}
            dep_breakup = pnl_data.get("depreciation_breakup") or {}
            if rev_breakup or dep_breakup:
                cursor.execute("""
                    INSERT INTO financial_revenue_breakup (cin, year, revenue_from_operations,
                        revenue_from_interest, revenue_from_other_financial_services,
                        revenue_from_sale_of_products, revenue_from_sale_of_services,
                        other_operating_revenues, excise_duty, depreciation, amortisation)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """, (cin, year, rev_breakup.get("revenue_from_operations"),
                      rev_breakup.get("revenue_from_interest"),
                      rev_breakup.get("revenue_from_other_financial_services"),
                      rev_breakup.get("revenue_from_sale_of_products"),
                      rev_breakup.get("revenue_from_sale_of_services"),
                      rev_breakup.get("other_operating_revenues"),
                      rev_breakup.get("excise_duty"),
                      dep_breakup.get("depreciation"),
                      dep_breakup.get("amortisation")))

        self.connection.commit()
        cursor.close()

    def _store_financial_parameters(self, cin, params_list):
        if not params_list:
            return
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM financial_parameters WHERE cin = %s", (cin,))
        for p in params_list:
            cursor.execute("""
                INSERT INTO financial_parameters (cin, year, nature, earning_fc, expenditure_fc,
                    transaction_related_parties_as_18, employee_benefit_expense, number_of_employees,
                    prescribed_csr_expenditure, total_amount_csr_spent_for_financial_year,
                    gross_fixed_assets, trade_receivable_exceeding_six_months, proposed_dividend)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, (cin, p.get("year", ""), p.get("nature", ""),
                  p.get("earning_fc"), p.get("expenditure_fc"),
                  p.get("transaction_related_parties_as_18"),
                  p.get("employee_benefit_expense"), p.get("number_of_employees"),
                  p.get("prescribed_csr_expenditure"),
                  p.get("total_amount_csr_spent_for_financial_year"),
                  p.get("gross_fixed_assets"),
                  p.get("trade_receivable_exceeding_six_months"),
                  p.get("proposed_dividend", "")))
        self.connection.commit()
        cursor.close()

    def _store_shareholdings(self, cin, shareholdings):
        if not shareholdings:
            return
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM shareholdings WHERE cin = %s", (cin,))
        for s in shareholdings:
            cursor.execute("""
                INSERT INTO shareholdings (cin, year, financial_year, category,
                    total_no_of_shares, promoter_shares, public_shares)
                VALUES (%s,%s,%s,%s,%s,%s,%s)
            """, (cin, s.get("year", ""), s.get("financial_year", ""), s.get("category", ""),
                  s.get("total_no_of_shares"), s.get("indian_held_no_of_shares"),
                  s.get("foreign_held_other_than_nri_no_of_shares")))
        self.connection.commit()
        cursor.close()

    def _store_gst(self, cin, gst_list):
        if not gst_list:
            return
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM gst_details WHERE cin = %s", (cin,))
        for g in gst_list:
            cursor.execute("""
                INSERT INTO gst_details (cin, gstin, status, company_name, trade_name,
                    state, date_of_registration, taxpayer_type)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            """, (cin, g.get("gstin", ""), g.get("status", ""), g.get("company_name", ""),
                  g.get("trade_name", ""), g.get("state", ""),
                  g.get("date_of_registration", ""), g.get("taxpayer_type", "")))
        self.connection.commit()
        cursor.close()

    def _store_legal(self, cin, legal_list):
        if not legal_list:
            return
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM legal_history WHERE cin = %s", (cin,))
        for l in legal_list:
            cursor.execute("""
                INSERT INTO legal_history (cin, petitioner, respondent, court, date,
                    case_status, case_number, case_type, case_category, severity)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, (cin, l.get("petitioner", ""), l.get("respondent", ""), l.get("court", ""),
                  l.get("date", ""), l.get("case_status", ""), l.get("case_number", ""),
                  l.get("case_type", ""), l.get("case_category", ""), l.get("severity", "")))
        self.connection.commit()
        cursor.close()

    def _store_charges(self, cin, charges_list):
        if not charges_list:
            return
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM charges WHERE cin = %s", (cin,))
        for c in charges_list:
            cursor.execute("""
                INSERT INTO charges (cin, charge_id, charge_holder, date_of_creation,
                    date_of_modification, amount, status)
                VALUES (%s,%s,%s,%s,%s,%s,%s)
            """, (cin, c.get("charge_id", ""), c.get("charge_holder", ""),
                  c.get("date_of_creation", ""), c.get("date_of_modification", ""),
                  c.get("amount"), c.get("status", "")))
        self.connection.commit()
        cursor.close()

    def _store_contacts(self, cin, contacts):
        if not contacts:
            return
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM contact_details WHERE cin = %s", (cin,))
        raw_emails = contacts.get("email", [])
        raw_phones = contacts.get("phone", [])
        # Handle both string lists and dict lists
        emails = ", ".join(
            e if isinstance(e, str) else e.get("email", str(e)) for e in raw_emails
        ) if isinstance(raw_emails, list) else ""
        phones = ", ".join(
            p if isinstance(p, str) else p.get("phone", str(p)) for p in raw_phones
        ) if isinstance(raw_phones, list) else ""
        cursor.execute("""
            INSERT INTO contact_details (cin, emails, phones) VALUES (%s,%s,%s)
        """, (cin, emails, phones))
        self.connection.commit()
        cursor.close()

    def _store_epfo(self, cin, epfo_list):
        if not epfo_list:
            return
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM epfo_establishments WHERE cin = %s", (cin,))
        for e in epfo_list:
            cursor.execute("""
                INSERT INTO epfo_establishments (cin, establishment_id, establishment_name,
                    working_status, date_of_setup, address, no_of_employees)
                VALUES (%s,%s,%s,%s,%s,%s,%s)
            """, (cin, e.get("establishment_id", ""), e.get("establishment_name", ""),
                  e.get("working_status", ""), e.get("date_of_setup", ""),
                  e.get("address", ""), e.get("no_of_employees")))
        self.connection.commit()
        cursor.close()

    def _store_credit_ratings(self, cin, ratings):
        if not ratings:
            return
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM credit_ratings WHERE cin = %s", (cin,))
        for r in ratings:
            cursor.execute("""
                INSERT INTO credit_ratings (cin, agency, instrument, rating, rating_date)
                VALUES (%s,%s,%s,%s,%s)
            """, (cin, r.get("agency", ""), r.get("instrument", ""),
                  r.get("rating", ""), r.get("rating_date", "")))
        self.connection.commit()
        cursor.close()

    def _store_rpt(self, cin, rpt_list):
        if not rpt_list:
            return
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM related_party_transactions WHERE cin = %s", (cin,))
        for rpt in rpt_list:
            fy = rpt.get("financial_year", "")
            for party_type in ["company", "llp", "individual", "others"]:
                for party in rpt.get(party_type, []):
                    cursor.execute("""
                        INSERT INTO related_party_transactions (cin, financial_year, party_name,
                            party_type, relationship, transaction_details)
                        VALUES (%s,%s,%s,%s,%s,%s)
                    """, (cin, fy, party.get("name", ""), party_type,
                          party.get("relationship", ""), str(party.get("transactions", ""))))
        self.connection.commit()
        cursor.close()

    def store_datastatus(self, cin, data_status):
        """Store data status for a company."""
        if not data_status:
            return
        cursor = self.connection.cursor()
        cursor.execute("""
            INSERT INTO data_status (cin, efiling_status, next_cin, last_base_updated,
                last_details_updated, last_fin_year_end, last_filing_date,
                last_annual_returns_year_end, last_epfo_updated)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ON DUPLICATE KEY UPDATE
                efiling_status=VALUES(efiling_status), next_cin=VALUES(next_cin),
                last_base_updated=VALUES(last_base_updated),
                last_details_updated=VALUES(last_details_updated),
                last_fin_year_end=VALUES(last_fin_year_end),
                last_filing_date=VALUES(last_filing_date),
                last_annual_returns_year_end=VALUES(last_annual_returns_year_end),
                last_epfo_updated=VALUES(last_epfo_updated)
        """, (cin, data_status.get("efiling_status", ""), data_status.get("next_cin"),
              data_status.get("last_base_updated", ""), data_status.get("last_details_updated", ""),
              data_status.get("last_fin_year_end", ""), data_status.get("last_filing_date", ""),
              data_status.get("last_annual_returns_year_end", ""),
              data_status.get("last_epfo_updated", "")))
        self.connection.commit()
        cursor.close()

    # --- Simple methods for backward compatibility ---

    def insert_company(self, cin, pan, company_name):
        cursor = self.connection.cursor()
        cursor.execute("""
            INSERT INTO companies (cin, pan, legal_name)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE pan=VALUES(pan), legal_name=VALUES(legal_name)
        """, (cin, pan, company_name))
        self.connection.commit()
        cursor.close()

    def insert_error(self, error_code, error_message, cin_queried):
        cursor = self.connection.cursor()
        cursor.execute("""
            INSERT INTO error_logs (error_code, error_message, cin_queried)
            VALUES (%s, %s, %s)
        """, (error_code, error_message, cin_queried))
        self.connection.commit()
        cursor.close()

    def get_company_by_cin(self, cin):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT cin, pan, legal_name as company_name FROM companies WHERE cin = %s", (cin,))
        result = cursor.fetchone()
        cursor.close()
        return result

    def get_latest_error_by_cin(self, cin):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(
            "SELECT error_code, error_message, cin_queried FROM error_logs WHERE cin_queried = %s ORDER BY id DESC LIMIT 1",
            (cin,))
        result = cursor.fetchone()
        cursor.close()
        return result

    def get_company_count_by_cin(self, cin):
        cursor = self.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM companies WHERE cin = %s", (cin,))
        count = cursor.fetchone()[0]
        cursor.close()
        return count

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
