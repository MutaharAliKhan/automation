class Queries:
    date_tl = "SELECT * FROM DATE_TL"

    user_tl = "SELECT * FROM USER_TL WHERE USER_ID = 'VDQATST1'"

    fetch_customer_and_account = '''SELECT
        digits(a.BRN_CD) AS BRANCH_CODE,
        digits(a.BRN_CD)|| '-' ||digits(a.AC_TYPE)|| '-' ||digits(a.CUST_NO)|| '-' ||digits(a.RUN_NO)|| '-' ||digits(a.CHK_DIGT) AS ACCOUNT_WITH_DASH_BRN,
        digits(a.BRN_CD)||digits(a.AC_TYPE)||digits(a.CUST_NO)||digits(a.RUN_NO)||digits(a.CHK_DIGT) AS ACCOUNT_BRN,
        digits(a.AC_TYPE)|| '-' ||digits(a.CUST_NO)|| '-' ||digits(a.RUN_NO)|| '-' ||digits(a.CHK_DIGT) AS ACCOUNT_WITH_DASH,
        digits(a.AC_TYPE)||digits(a.CUST_NO)||digits(a.RUN_NO)||digits(a.CHK_DIGT) AS ACCOUNT,
        digits(a.CUST_NO) AS CUSTOMER_NO,
        digits(a.AC_TYPE) AS ACCOUNT_TYPE,
        digits(a.RUN_NO) AS RUN_NO,
        digits(a.CHK_DIGT) AS CHECK_DIGIT,
        digits(c.START_NO) AS CHEQUE_NO,
        c.STATUS_0 AS CHEQUE_STATUS,
        a.HASH_BAL AS BALANCE
        FROM
            account_tl AS a 
            LEFT JOIN CHQBK_TL c
            ON (a.BRN_CD, a.AC_TYPE, a.CUST_NO, a.RUN_NO, a.CHK_DIGT) = (c.BRN_CD, c.AC_TYPE, c.CUST_NO, c.RUN_NO, c.CHK_DIGT)
        WHERE
            a.BRN_CD = ?
            AND a.CCY_CD = 586
            AND a.AC_TYPE in (71,81,981)
            AND a.HASH_BAL >= '1000000'
            AND a.LEDG_BAL >= '1000000'
            AND a.LOC_EQV >= '1000000'
            AND c.STATUS_0 = 'U'
            AND a.CUST_NO in (SELECT CUST_NO from Customer_tl where BRN_CD = a.BRN_CD and Filer = 'Y' )
            AND a.CUST_NO not in (SELECT CUST_NO FROM ACC_COND_TL where BRN_CD = a.BRN_CD 
            AND AC_TYPE = a.AC_TYPE 
            AND CUST_NO = a.CUST_NO
            AND RUN_NO  = a.RUN_NO
            AND CHK_DIGT = a.CHK_DIGT
            AND CND_CD IN (13,14,18,16))
        ORDER BY
            RAND
        LIMIT 1'''

    fetch_customer = '''SELECT
        digits(a.BRN_CD) AS BRANCH_CODE,
        digits(a.BRN_CD)|| '-' ||digits(a.AC_TYPE)|| '-' ||digits(a.CUST_NO)|| '-' ||digits(a.RUN_NO)|| '-' ||digits(a.CHK_DIGT) AS ACCOUNT_WITH_DASH_BRN,
        digits(a.BRN_CD)||digits(a.AC_TYPE)||digits(a.CUST_NO)||digits(a.RUN_NO)||digits(a.CHK_DIGT) AS ACCOUNT_BRN,
        digits(a.AC_TYPE)|| '-' ||digits(a.CUST_NO)|| '-' ||digits(a.RUN_NO)|| '-' ||digits(a.CHK_DIGT) AS ACCOUNT_WITH_DASH,
        digits(a.AC_TYPE)||digits(a.CUST_NO)||digits(a.RUN_NO)||digits(a.CHK_DIGT) AS ACCOUNT,
        digits(a.CUST_NO) AS CUSTOMER_NO,
        digits(a.AC_TYPE) AS ACCOUNT_TYPE,
        digits(a.RUN_NO) AS RUN_NO,
        digits(a.CHK_DIGT) AS CHECK_DIGIT,
        digits(c.START_NO) AS CHEQUE_NO,
        a.IBAN as IBAN_NUMBER,
        a.CCY_CD as CURRENCY,
        c.STATUS_0 AS CHEQUE_STATUS,
        a.HASH_BAL AS BALANCE
        FROM
            account_tl AS a 
            LEFT JOIN CHQBK_TL c
            ON (a.BRN_CD, a.AC_TYPE, a.CUST_NO, a.RUN_NO, a.CHK_DIGT) = (c.BRN_CD, c.AC_TYPE, c.CUST_NO, c.RUN_NO, c.CHK_DIGT)
        WHERE
            a.BRN_CD = ?
            AND a.CCY_CD = ?
            AND a.AC_TYPE = ?
          	AND a.HASH_BAL >= '50000'
            AND c.STATUS_0 = 'U'
            AND a.CUST_NO in (SELECT CUST_NO from Customer_tl where BRN_CD = a.BRN_CD and Filer = 'N' )
            AND a.CUST_NO not in (SELECT CUST_NO FROM ACC_COND_TL where BRN_CD = a.BRN_CD
            AND CND_CD IN (13,14,18,16))
        ORDER BY
            RAND
        LIMIT 1'''

    fetch_company_and_collection_account = '''select 
    a.C_BRN_CD,
    a.BRN_CD,
    REPLACE(b.NAME,'&','\\&') as COMPANY_NAME,
    digits(a.C_AC_TYPE) ||''||digits(a.C_CUST_NO)||''||digits(a.C_RUN_NO) as COLLECTION_ACCOUNT 
    from CMGMT_COMP_AC_TL a 
    join CMGMT_COMP_INFO b  
    on a.BRN_CD = b.BRN_CD and a.AC_TYPE = b.AC_TYPE 
    and a.CUST_NO = b.CUST_NO 
    and a.CHK_DIGT = b.CHK_DIGT 
    and a.RUN_NO = b.RUN_NO
    where b.BRN_CD = ? order by rand Limit 1'''

    fetch_current_date = '''SELECT 
    TDATE AS TODAY_DATE,
    VARCHAR_FORMAT(TDATE, 'DD/MM/YYYY') AS TODAY_DATE_FORMATTED
    FROM DATE_TL WHERE BRN_CD = ? limit 1
    '''

    update_user_system_ip = '''update USER_TL set USER_IPADDR = ? where BRN_CD = ? and USER_ID in 
    ('VDQATST1','VDQAUTH1')
    '''

    fetch_credit_card_number = '''select digits(CARD_NO) as CREDIT_CARD_NO from CC_ACC_CARDS_TL 
    where CARD_NO like ('%5121760%') order by rand Limit 1'''

    update_target_branch_date = '''update date_tl set TDATE = ? where BRN_CD = ?'''

    fetch_target_branch = '''select digits(BRN_CD) As TARGET_BRANCH_CODE from BRANCHTL WHERE BRN_CD BETWEEN 1 AND 5999
    AND BRN_CD not in (1999,786,787,883,4445) and BNK_CD = 1 and CENT_BRN = 'Y' ORDER BY RAND LIMIT 1'''

    fetch_dividend_warrant_and_folio_num = '''Select digits(b.BRN_CD) as BRN_CD,digits(a.C_BRN_CD) as C_BRN_CD,
    digits(a.C_AC_TYPE) as C_AC_TYPE,digits(a.C_CUST_NO) as C_CUST_NO,digits(a.C_RUN_NO) as C_RUN_NO,
    digits(a.C_CHK_DIGT) as C_CHK_DIGT ,a.AMOUNT,a.FOLIO_NO,a.WARRANT_NO,b.AC_TITLE as COMPANY from DIV_WRNT_INFO_TL 
    a join DIV_AC_TL b on (a.C_BRN_CD,a.DIV_ISS_NO,a.C_AC_TYPE,a.C_CUST_NO,a.C_RUN_NO,a.C_CHK_DIGT) = (b.C_BRN_CD,
    b.DIV_ISS_NO,b.C_AC_TYPE,b.C_CUST_NO,b.C_RUN_NO,b.C_CHK_DIGT) where  a.WARRANT_STS = 'U' and b.BRN_CD = ? and not 
    REGEXP_LIKE(a.FOLIO_NO, '[[:alpha:]]')  order by rand limit 1'''

    fetch_dividend_warrant_and_folio_num_for_rw = '''Select digits(BRN_CD) as CUST_BRN_CD,digits(a.C_BRN_CD) as C_BRN_CD,digits(a.C_AC_TYPE) as C_AC_TYPE,digits(a.C_CUST_NO) as C_CUST_NO,
    digits(a.C_RUN_NO) as C_RUN_NO,digits(a.C_CHK_DIGT) as C_CHK_DIGT ,cast(a.AMOUNT as INTEGER) as AMOUNT,
    a.FOLIO_NO,a.WARRANT_NO,b.AC_TITLE as COMPANY from DIV_WRNT_INFO_TL a join DIV_AC_TL b 
    on (a.C_BRN_CD,a.DIV_ISS_NO,a.C_AC_TYPE,a.C_CUST_NO,a.C_RUN_NO,a.C_CHK_DIGT,a.DIV_ISS_NO) 
    = (b.C_BRN_CD,b.DIV_ISS_NO,b.C_AC_TYPE,b.C_CUST_NO,b.C_RUN_NO,b.C_CHK_DIGT,b.DIV_ISS_NO) 
    where  a.WARRANT_STS = 'U' and a.C_BRN_CD = ? and a.FOLIO_NO not like REGEXP_LIKE(a.FOLIO_NO, 
    '[[:alpha:]]') limit 1
    '''

    update_dividend_warrant_status = '''UPDATE DIV_WRNT_INFO_TL set EXPIRY_DT = '2050-05-19' where C_BRN_CD = ? and 
    FOLIO_NO = ?'''

    delete_acc_cond_tl = '''DELETE FROM ACC_COND_TL WHERE BRN_CD = ? AND CUST_NO = ? AND CND_CD in (13,15,16,18,19)'''

    update_account_balance = '''UPDATE ACCOUNT_TL SET LEDG_BAL=10000000 , LOC_EQV=10000000, HASH_BAL=10000008 , 
                 SHADOW_C=0,SHADOW_D=0  , AMT_BLK = 0  ,  UNCL_AMT =  0  , LIM_AMT= 0 ,IN_ACR_C = NULL , IN_ACR_D = NULL 
                 WHERE  BRN_CD = ? and Cust_no = ?'''

    check_user_exists = '''select Count (*) as USER_ID from USER_tl where USER_ID = ? and BRN_CD = ?'''

    user_insertion = '''INSERT INTO DB2ADMIN.USER_TL
                (BRN_CD, USER_ID, PASSWORD, LTPSCHDT, LTSGONDT, INV_ATMP, ENB_DIS, GROUP_CD, DEPT_NO, SIGNONST, PS_EX_DATE, ASSIGN_BY, CRTN_DATE, P_LMT_C_AC_CASH_DR_NAT, P_LMT_C_AC_CASH_CR_NAT, P_LMT_C_AC_CLR_DR_NAT, P_LMT_C_AC_CLR_CR_NAT, P_LMT_C_AC_TR_DR_NAT, P_LMT_C_AC_TR_CR_NAT, P_LMT_GL_AC_DR_NAT, P_LMT_GL_AC_CR_NAT, P_LMT_MO_AC_DR_NAT, P_LMT_MO_AC_CR_NAT, P_LMT_N_V_INT_AC_DR_NAT, P_LMT_N_V_INT_AC_CR_NAT, EP_LMT_C_AC_CASH_DR, EP_LMT_C_AC_CASH_CR, EP_LMT_C_AC_CLR_DR, EP_LMT_C_AC_CLR_CR, EP_LMT_C_AC_TR_DR, EP_LMT_C_AC_TR_CR, EP_LMT_GL_AC_DR, EP_LMT_GL_AC_CR, EP_LMT_MO_AC_DR, EP_LMT_MO_AC_CR, EP_LMT_N_V_INT_AC_DR, EP_LMT_N_V_INT_AC_CR, OD_AUTH_LMT_CUST_AC, OD_AUTH_LMTN_V_INT_AC, OD_AUTH_LMT_MO_AC, P_LMT_C_AC_CASH_DR_REM, P_LMT_C_AC_CASH_CR_REM, P_LMT_C_AC_CLR_DR_REM, P_LMT_C_AC_CLR_CR_REM, P_LMT_C_AC_TR_DR_REM, P_LMT_C_AC_TR_CR_REM, P_LMT_GL_AC_DR_REM, P_LMT_GL_AC_CR_REM, P_LMT_MO_AC_DR_REM, P_LMT_MO_AC_CR_REM, P_LMT_N_V_INT_AC_DR_REM, P_LMT_N_V_INT_AC_CR_REM, ACCESS_DORMANT_AC, ACCESS_CLASSIFED_AC, ACCESS_DECEASED_AC, ACCESS_MAN_LEDGER, ACCESS_FROZEN_AC, ATTORNEY_NO, ATTORNEY_CLASS, REMARKS, USER_NAME, EMP_NO, EXP_DAYS, DESIGNATION, NON_FIN_AUTH_VALUE, MULTI_BR_FIN_TR_ALLOWED, MULTI_BR_NFIN_TR_ALLOWED, PS_STATUS, AUTHORIZED_BY, CERTIFY_DATE, USER_IPADDR, CERTIFY_BY, CERTIFY_AUTHBY, SYSTEM_USR, REASON_CD, ACT_DEACT, ACT_REASON_CD, ACT_REASON_DESC, ACT_DATE, EVNG_BNKNG)
                VALUES(?, ?, ?, TO_DATE('2999-07-01','YYYY-MM-DD'), TO_DATE('2999-07-01','YYYY-MM-DD'), 0, 'E', 'ALLUSERGRP', 2, 'N', TO_DATE('2999-07-01','YYYY-MM-DD'), 'VALUSER', TO_DATE('2999-07-01','YYYY-MM-DD'), 5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000, 'Y', 'Y', 'Y', 'Y', 'Y', NULL, NULL, '1.00E+11', 'VALIDATION AUTHORIZER', 99999, 30, 'OFFICER GRADE I               ', 0, 'N', 'N', NULL, 'TERESOL', TO_DATE('2999-07-01','YYYY-MM-DD'), '', 'TERESOL', 'TERESOL', 'N', 0, 'A', NULL, NULL, NULL, 'N');'''

    auth_user_insertion = '''INSERT INTO DB2ADMIN.USER_TL
                (BRN_CD, USER_ID, PASSWORD, LTPSCHDT, LTSGONDT, INV_ATMP, ENB_DIS, GROUP_CD, DEPT_NO, SIGNONST, PS_EX_DATE, ASSIGN_BY, CRTN_DATE, P_LMT_C_AC_CASH_DR_NAT, P_LMT_C_AC_CASH_CR_NAT, P_LMT_C_AC_CLR_DR_NAT, P_LMT_C_AC_CLR_CR_NAT, P_LMT_C_AC_TR_DR_NAT, P_LMT_C_AC_TR_CR_NAT, P_LMT_GL_AC_DR_NAT, P_LMT_GL_AC_CR_NAT, P_LMT_MO_AC_DR_NAT, P_LMT_MO_AC_CR_NAT, P_LMT_N_V_INT_AC_DR_NAT, P_LMT_N_V_INT_AC_CR_NAT, EP_LMT_C_AC_CASH_DR, EP_LMT_C_AC_CASH_CR, EP_LMT_C_AC_CLR_DR, EP_LMT_C_AC_CLR_CR, EP_LMT_C_AC_TR_DR, EP_LMT_C_AC_TR_CR, EP_LMT_GL_AC_DR, EP_LMT_GL_AC_CR, EP_LMT_MO_AC_DR, EP_LMT_MO_AC_CR, EP_LMT_N_V_INT_AC_DR, EP_LMT_N_V_INT_AC_CR, OD_AUTH_LMT_CUST_AC, OD_AUTH_LMTN_V_INT_AC, OD_AUTH_LMT_MO_AC, P_LMT_C_AC_CASH_DR_REM, P_LMT_C_AC_CASH_CR_REM, P_LMT_C_AC_CLR_DR_REM, P_LMT_C_AC_CLR_CR_REM, P_LMT_C_AC_TR_DR_REM, P_LMT_C_AC_TR_CR_REM, P_LMT_GL_AC_DR_REM, P_LMT_GL_AC_CR_REM, P_LMT_MO_AC_DR_REM, P_LMT_MO_AC_CR_REM, P_LMT_N_V_INT_AC_DR_REM, P_LMT_N_V_INT_AC_CR_REM, ACCESS_DORMANT_AC, ACCESS_CLASSIFED_AC, ACCESS_DECEASED_AC, ACCESS_MAN_LEDGER, ACCESS_FROZEN_AC, ATTORNEY_NO, ATTORNEY_CLASS, REMARKS, USER_NAME, EMP_NO, EXP_DAYS, DESIGNATION, NON_FIN_AUTH_VALUE, MULTI_BR_FIN_TR_ALLOWED, MULTI_BR_NFIN_TR_ALLOWED, PS_STATUS, AUTHORIZED_BY, CERTIFY_DATE, USER_IPADDR, CERTIFY_BY, CERTIFY_AUTHBY, SYSTEM_USR, REASON_CD, ACT_DEACT, ACT_REASON_CD, ACT_REASON_DESC, ACT_DATE, EVNG_BNKNG)
                VALUES(?, ?, ?, TO_DATE('2999-07-01','YYYY-MM-DD'), TO_DATE('2999-07-01','YYYY-MM-DD'), 0, 'E', 'ALLUSERGRP', 2, 'N', TO_DATE('2999-07-01','YYYY-MM-DD'), 'VALUSER', TO_DATE('2999-07-01','YYYY-MM-DD'), 10000000000000, 10000000000000, 10000000000000, 10000000000000, 10000000000000, 10000000000000, 10000000000000, 10000000000000, 10000000000000, 10000000000000, 10000000000000, 10000000000000, 10000000000000, 10000000000000, 10000000000000, 10000000000000, 10000000000000, 10000000000000, 10000000000000, 10000000000000, 10000000000000, 10000000000000, 10000000000000, 10000000000000, 10000000000000, 10000000000000, 10000000000000, 10000000000000, 10000000000000, 10000000000000, 10000000000000, 10000000000000, 10000000000000, 10000000000000, 10000000000000, 10000000000000, 10000000000000, 10000000000000, 10000000000000, 'N', 'N', 'N', 'N', 'N', NULL, NULL, '1.00E+11', 'VALIDATION AUTHORIZER', 99999, 30, 'OFFICER GRADE I               ', 0, 'N', 'N', NULL, 'TERESOL', TO_DATE('2999-07-01','YYYY-MM-DD'), '', 'TERESOL', 'TERESOL', 'N', 0, 'A', NULL, NULL, NULL, 'N');'''

    assign_rights_to_users = '''INSERT INTO USER_ACT_AUTH_TL SELECT ? ,MOD_CD,ACTIVITY_CD, ? FROM MODAVTVTL WHERE  MOD_CD IN (SELECT MOD_CD FROM MODUL_TL) AND ACTIVITY_CD NOT IN (SELECT ACTIVITY_CD FROM USER_ACT_AUTH_TL WHERE USER_ID = ? AND BRN_CD = ?)'''

    get_brn_name_and_code = '''select b.BRN_NAME ||'-' || digits(b.BRN_CD) as BRN_NAME_AND_CD from BRANCHTL b where b.BRN_CD = ? and BNK_CD = 1 limit 1'''
    get_brn_code_and_name = '''select digits(b.BRN_CD) ||'-' ||b.BRN_NAME  as BRN_CD_AND_NAME from BRANCHTL b where b.BRN_CD = ? and BNK_CD = 1 limit 1'''
    get_debarred_cnic = '''select ID_DOC_NO from DEBARRED_LIST_TL where ID_DOC_TYPE = 'CNIC' order by rand limit 1'''
    get_debarred_passport = '''select ID_DOC_NO from DEBARRED_LIST_TL where ID_DOC_TYPE = 'PASSPORT' order by rand limit 1'''
    fetch_company_details = '''Select COMPANY_ORG_NAME,company_id || '-' || REPLACE(company_name,'&','\\&') as DropDownValue,SUBSTRING(COMP_ACC,1,4) as BRN_CD ,SUBSTRING(COMP_ACC,6,3) as AC_TYPE, 
                            SUBSTRING(COMP_ACC,10,6) as CUST_NO,SUBSTRING(COMP_ACC,17,2)as RUN_NO , SUBSTRING(COMP_ACC,20,1)as CHKDIGIT from company_barcode_tl where COMPANY_NAME = ?'''
    fetch_billing_month = '''select MONTHNAME ((TDate) - 60, 'CLDR181_en_US') || '-' || Year(TDate) as FIR, MONTHNAME ((TDate) - 30, 'CLDR181_en_US') || '-' || Year(TDate) as SEC,
                                MONTHNAME (TDate, 'CLDR181_en_US') || '-' || Year(TDate) as TIR , BRN_CD ,TDate from date_tl where brn_cd =  ?'''

    check_collection_acc_against_branch = '''SELECT count(LCL_BRN_CD) as EXIST FROM CMGMT_COMP_INFO where NAME = ? and LCL_BRN_CD = ?'''


query = Queries()
