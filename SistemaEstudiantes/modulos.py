def Select():
     sql="SELECT * FROM `estudiantes`;"
     return sql

def Delete():
    sql="DELETE FROM estudiantes where id=%s"
    return sql

def Insert():
     sql="INSERT INTO `estudiantes` (`id`, `nombre`, `apellido`, `correo`, `ncontrol`, `carrera`, `foto`) VALUES (NULL, %s,%s,%s,%s,%s,%s);"
     return sql