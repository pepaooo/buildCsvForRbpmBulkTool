import csv


def generar_csv_asignaciones(input_file, output_file):
    # Diccionario para almacenar {user_dn: set([rol_dn1, rol_dn2, ...])}
    user_roles = {}

    # Lectura del archivo CSV de entrada
    with open(input_file, 'r', newline='', encoding='utf-8') as f_in:
        # DictReader asume que la primera línea del CSV contiene los nombres de columna
        reader = csv.DictReader(f_in, delimiter='\t')

        for row in reader:
            print(row)

            # Obtenemos los valores de las columnas 'cn-role-10' y 'member'
            role_dn = row.get('cn-role-10', '')

            # La columna 'member' puede contener varios usuarios separados por '|'
            members_str = row.get('member', '')

            if not members_str.strip():
                # Si no hay valor en la columna 'member', puedes saltar o manejar de otro modo:
                # continue
                members = []
            else:
                members = members_str.strip().split('|')

            for member_dn in members:
                member_dn = member_dn.strip()
                if member_dn not in user_roles:
                    user_roles[member_dn] = set()

                # 1) Agregamos el rol original
                user_roles[member_dn].add(role_dn)

                # 2) Condición para agregar el rol adicional si corresponde
                if role_dn.startswith("cn=IMAN-"):
                    user_roles[member_dn].add(
                        "cn=IDM-Account-IMAN,cn=Level10,cn=RoleDefs,cn=RoleConfig,cn=AppConfig,cn=User Application Driver,cn=DriverSet1,ou=idm,ou=services,o=system")
                elif role_dn.startswith("cn=ICON-"):
                    user_roles[member_dn].add(
                        "cn=IDM-Account-ICON,cn=Level10,cn=RoleDefs,cn=RoleConfig,cn=AppConfig,cn=User Application Driver,cn=DriverSet1,ou=idm,ou=services,o=system")
                elif role_dn.startswith("cn=IDGOV-"):
                    user_roles[member_dn].add(
                        "cn=IDM-Account-IDGOV,cn=Level10,cn=RoleDefs,cn=RoleConfig,cn=AppConfig,cn=User Application Driver,cn=DriverSet1,ou=idm,ou=services,o=system")
                elif role_dn.startswith("cn=GPOIDM-"):
                    user_roles[member_dn].add(
                        "cn=IDM-Account-GPOIDM,cn=Level10,cn=RoleDefs,cn=RoleConfig,cn=AppConfig,cn=User Application Driver,cn=DriverSet1,ou=idm,ou=services,o=system")
                elif role_dn.startswith("cn=IDAPPS-"):
                    user_roles[member_dn].add(
                        "cn=IDM-Account-IDAPPS,cn=Level10,cn=RoleDefs,cn=RoleConfig,cn=AppConfig,cn=User Application Driver,cn=DriverSet1,ou=idm,ou=services,o=system")
                elif role_dn.startswith("cn=IDRPT-"):
                    user_roles[member_dn].add(
                        "cn=IDM-Account-IDRPT,cn=Level10,cn=RoleDefs,cn=RoleConfig,cn=AppConfig,cn=User Application Driver,cn=DriverSet1,ou=idm,ou=services,o=system")

    # Escritura del archivo CSV de salida
    with open(output_file, 'w', newline='', encoding='utf-8') as f_out:
        writer = csv.writer(f_out, quoting=csv.QUOTE_ALL)

        # Por cada usuario, unimos todos sus roles con '###'
        for user_dn, roles_set in user_roles.items():
            roles_str = '###'.join(sorted(roles_set))  # sorted() opcional, por legibilidad
            # Estructura de la fila de salida
            # "assigntouser","<user_dn>","<roles_separados_por_###>","Asignación por carga inicial", ...
            row = [
                "assigntouser",
                user_dn,
                roles_str,
                "Asignación por carga inicial",
                "", "", "", "", "", "", "", "", ""
            ]
            writer.writerow(row)


if __name__ == "__main__":
    # Ajusta los nombres de archivo según tu preferencia
    archivo_entrada = "entrada.csv"
    archivo_salida = "salida.csv"

    generar_csv_asignaciones(archivo_entrada, archivo_salida)
    print(f"Archivo de salida generado: {archivo_salida}")
