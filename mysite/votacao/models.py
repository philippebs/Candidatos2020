from django.db import models

# Create your models here.
class TipoCandidato(models.Model):
    nome = models.CharField(max_length=200)


    def __str__(self):
        return self.nome


class Partido(models.Model):
    nome = models.CharField(max_length=200)
    numero = models.IntegerField()

    def __str__(self):
        return self.nome + ' ' + str(self.numero)


class Municipio(models.Model):
    nome = models.CharField(max_length=200)
    numero = models.IntegerField()

    def __str__(self):
        return self.nome + ' ' + str(self.numero)


class MunicipioZona(models.Model):
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE)
    zona = models.IntegerField()
    secao = models.IntegerField()

    def __str__(self):
        return self.municipio.nome + ' ' + str(self.zona) + ' - ' +  str(self.secao)


class Candidato(models.Model):
    nome = models.CharField(max_length=200)

    def __str__(self):
        return self.nome


class CandidatoPartido(models.Model):
    nome = models.CharField(max_length=200)
    numero = models.IntegerField()
    ano = models.IntegerField()
    candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE)
    partido = models.ForeignKey(Partido, on_delete=models.CASCADE)
    tipo_candidato = models.ForeignKey(TipoCandidato, on_delete=models.CASCADE)
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE)


class Voto(models.Model):
    candidato_partido = models.ForeignKey(CandidatoPartido, on_delete=models.CASCADE)
    municipio_zona = models.ForeignKey(MunicipioZona, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    turno = models.IntegerField()

