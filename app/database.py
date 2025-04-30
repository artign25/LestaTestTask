from sqlalchemy import Column, Integer, String, MetaData, Table, ForeignKey
from sqlalchemy.ext.asyncio import create_async_engine

async_engine = create_async_engine(
    "sqlite+aiosqlite:///database.db",
    echo=True,
    pool_size=10,
    max_overflow=10,
)

metadata_obj = MetaData()

text_files_table = Table(
    "text_files",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("file_name", String)
)

files_data_table = Table(
    "files_data",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("word", String),
    Column("tf", Integer),
    Column("idf", Integer),
    Column("file_id", Integer, ForeignKey("text_files.id")),
)


async def recreate_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(metadata_obj.drop_all)
        await conn.run_sync(metadata_obj.create_all)


async def add_text_file_data(file_name, file_data):
    async with async_engine.connect() as conn:
        text_stmt = text_files_table.insert().values(
            [
                {"file_name": file_name}
            ]
        ).returning(text_files_table.c.id)
        added_file = await conn.execute(text_stmt)
        file_id = added_file.first()[0]
        file_data = [
            {
                "word": word.word,
                "tf": word.tf,
                "idf": word.idf,
                "file_id": file_id,
            } for word in file_data]
        data_stmt = files_data_table.insert().values(
            file_data
        )
        await conn.execute(data_stmt)
        await conn.commit()
