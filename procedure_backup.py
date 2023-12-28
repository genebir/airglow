from sqlalchemy import create_engine
import os
import datetime
"""
프로시져 백업

저장폴더는 해당 소스 경로에 생성됩니다.
저장폴더명은 운영계는 prd, 개발계는 dev로 생성됩니다.

프로시져를 백업하는 파일명은
스키마명.프로시져명.sql 로 생성됩니다.

프로시져를 백업하는 파일은 해당 DB의 프로시져를 백업하는 파일이므로
운영계에서는 운영계 DB의 프로시져를 백업하는 파일이 생성되고
개발계에서는 개발계 DB의 프로시져를 백업하는 파일이 생성됩니다.

"""


engine = create_engine(f'postgresql://tcb_trt_mwaa_ap:Ptrtapmwaa2!@cb-prd-trt-db.cluster-c1cc9czlzwdp.ap-northeast-2.rds.amazonaws.com:5432/ptcbtrtdb') # 운영계 connection
directory = 'prd' # 저장폴더
# engine = create_engine(f'postgresql://tcb_trt_mwaa_ap:Dtrtapmwaa2!@cb-dev-all-db.cluster-ccf5oucpbjvb.ap-northeast-2.rds.amazonaws.com:5432/dtcbtrtdb') # 개발계 connection
# directory = 'dev' # 저장폴더

query = """
SELECT  n.nspname		as schema
	, upper(c.proname)	as procedure_name
	, d.description		as procedure_description
	, c.proargnames		as procedure_arg_names
	, c.prosrc 			as procedure_source
FROM pg_catalog.pg_proc AS c
LEFT JOIN pg_catalog.pg_description AS d ON c.oid = d.objoid --  AND a.attnum = d.objsubid
JOIN pg_catalog.pg_namespace        AS n ON c.pronamespace  = n.oid
WHERE 1=1
AND c.prokind = 'p'		-- 프로시져만
AND n.nspname in ('tcb_co_db','tcb_dc_db','tcb_dm_db')
-- AND c.proname not like 'x_%%'
ORDER BY n.nspname, c.proname;
"""

data = engine.execute(query).fetchall()
print(data)

if os.path.exists(directory):
    if not os.path.exists(f'{directory}_xxx'):
        os.makedirs(f'{directory}_xxx')
    backup_dir = f"{directory}_xxx/{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    os.makedirs(backup_dir)
    import shutil
    shutil.move(f'{directory}/', backup_dir)
if not os.path.exists(directory):
    os.makedirs(directory)

# create절과 comment, alter, grant절을 위 아래에 추가
for _ in data:
    create_query = f"""create procedure {_[1].lower()}({", ".join([f"IN {x} character" for x in _[3]]) if _[3] is not None else ""})
\tlanguage plpgsql
as
$$
    """

    comment_query = f"""\n
comment on procedure {_[1].lower()}({", ".join([f"char" for _ in _[3]]) if _[3] is not None else ""}) is '{_[2]}';

alter procedure {_[1].lower()}({", ".join([f"char" for _ in _[3]]) if _[3] is not None else ""}) owner to tcb_trt_db_admin;

grant execute on procedure {_[1].lower()}({", ".join([f"char" for _ in _[3]]) if _[3] is not None else ""}) to tcb_dc_db_admin;

grant execute on procedure {_[1].lower()}({", ".join([f"char" for _ in _[3]]) if _[3] is not None else ""}) to tcb_dc_db_dml;
    """
    # create절 + 프로시져 소스 + comment절
    result = create_query + _[4] + "$$;" + comment_query
    print(result)
    with open(f"{directory}/{_[0]}.{_[1].lower()}.sql", 'w') as f:
        f.write(result)

