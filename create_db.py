from application import auth
from database import Usuario, Producto, Consumo


def main():
    Usuario.create_table(fail_silently=True)
    Producto.create_table(fail_silently=True)
    Consumo.create_table(fail_silently=True)
    auth.User.create_table(fail_silently=True)  # make sure table created.
#    admin = auth.User(username='admin', email='', admin=True, active=True)
#    admin.set_password('admin')
#    admin.save()


if __name__ == '__main__':
    main()
