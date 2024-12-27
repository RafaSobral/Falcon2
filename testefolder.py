import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

# Configurações do S3
AWS_ACCESS_KEY_ID = 'AKIAZ7SALK5PMRSG2BWC'
AWS_SECRET_ACCESS_KEY = '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'
AWS_BUCKET_NAME = 'falcon-aws-bucket'
AWS_REGION = 'sa-east-1'  # Ex.: 'us-east-1' ou 'sa-east-1'


def upload_test_file():
    # Cria o cliente S3
    s3 = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION
    )

    try:
        # Cria um arquivo fictício em memória
        file_content = "Este é um teste de upload para o S3.".encode("utf-8")  # Corrigido para usar encode UTF-8
        file_name = "teste.txt"

        # Faz o upload do arquivo para o bucket
        s3.put_object(Bucket=AWS_BUCKET_NAME, Key=file_name, Body=file_content)

        # URL pública do arquivo (se o bucket permitir acesso público)
        file_url = f"https://{AWS_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{file_name}"
        print(f"Arquivo enviado com sucesso! URL: {file_url}")

    except NoCredentialsError:
        print("Erro: Credenciais da AWS não fornecidas ou inválidas.")
    except PartialCredentialsError:
        print("Erro: Credenciais incompletas fornecidas.")
    except Exception as e:
        print(f"Erro ao enviar o arquivo: {e}")

# Executa o teste
if __name__ == "__main__":
    upload_test_file()
