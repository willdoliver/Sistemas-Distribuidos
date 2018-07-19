package criptografia;

import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.security.InvalidKeyException;
import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.NoSuchAlgorithmException;
import java.security.PrivateKey;
import java.security.PublicKey;
import javax.crypto.BadPaddingException;
import javax.crypto.Cipher; 
import javax.crypto.IllegalBlockSizeException; 
import javax.crypto.NoSuchPaddingException;



public class Criptografia {
    
    public class RsaCipher {

    private final PublicKey publicKey;
    private final PrivateKey privateKey;

    public RsaCipher(PublicKey publicKey, PrivateKey privateKey) {
        this.publicKey = publicKey;
        this.privateKey = privateKey;
    }

    public KeyPair genKeyPair() throws NoSuchAlgorithmException {
        KeyPairGenerator generator = KeyPairGenerator.getInstance("RSA");
        generator.initialize(512);
        KeyPair keyPair = generator.generateKeyPair();

        return keyPair;
    }

    public String encrypt(String string) throws InvalidKeyException, NoSuchPaddingException, NoSuchAlgorithmException, BadPaddingException, IllegalBlockSizeException {
        Cipher cipher = Cipher.getInstance("RSA");
        cipher.init(Cipher.ENCRYPT_MODE, privateKey);
        return new String(cipher.doFinal(string.getBytes()));
    }

    public String decrypt(String string) throws NoSuchPaddingException, NoSuchAlgorithmException, InvalidKeyException, IOException, BadPaddingException, IllegalBlockSizeException {
        Cipher cipher = Cipher.getInstance("RSA");
        cipher.init(Cipher.DECRYPT_MODE, publicKey);
        return new String(cipher.doFinal(string.getBytes()));
    }
}

    public static void main(String[] args) throws NoSuchAlgorithmException, NoSuchPaddingException, InvalidKeyException, IllegalBlockSizeException, BadPaddingException, UnsupportedEncodingException {
    
        String leitura = null;
        
        //leitura do arquivo .txt
        Path caminho = Paths.get("C:/Users/GM/Documents/NetBeansProjects/criptografia/Arquivos/teste.txt");
        try{
           byte[] texto = Files.readAllBytes(caminho);
           leitura = new String(texto);
           System.out.println("Arquivo original: " + leitura);
        } catch(Exception erro){System.out.println("Erro ao ler arquivo");}
        
        
        //escrita do arquivo .txt
        Path caminho2 = Paths.get("C:/Users/GM/Documents/NetBeansProjects/criptografia/Arquivos/teste_recebe.txt");
        String texto2 = new String(leitura);
        byte[] textoByte = texto2.getBytes();
        try{
            Files.write(caminho2, textoByte);
        }catch(Exception erro){System.out.println("Erro em salvar arquivo");}
        
        
    /*--------------------------------------------------------------------------*/
    /*-----------------------------Criptografia---------------------------------*/
    
    //Gerando as chaves
    KeyPairGenerator generator = KeyPairGenerator.getInstance("RSA");
    generator.initialize(512);
    KeyPair keyPair = generator.generateKeyPair();
    
    //Captura das chaves
    PrivateKey privateKey = keyPair.getPrivate();
    PublicKey publicKey = keyPair.getPublic();
    
    //Capturar da instância de Cipher, que irá realizar a criptografia e decriptografia
    final Cipher cipher = Cipher.getInstance("RSA");
    
    //Modos para criptografia e descriptografia
    cipher.init(Cipher.ENCRYPT_MODE, privateKey);
    
    byte[] criptografado = cipher.doFinal(leitura.getBytes());
    System.out.println("Arquivo criptografado: " + criptografado);
    
    cipher.init(Cipher.DECRYPT_MODE, publicKey);
    byte[] descriptografado = cipher.doFinal(criptografado);
    System.out.println("Arquivo descriptografado: " + new String(descriptografado));
    
    }//fim do main
    
}
