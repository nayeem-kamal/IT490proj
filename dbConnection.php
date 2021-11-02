<?php 

//Establishes SQL connection with 

function dbConnection()
{
    $hostname = '127.0.0.1';
    $user = 'root';
    $password = 'toor';
    $name = 'it490';

    $connection = mysqli_connect($hostname, $user, $password, $name)

    if (!$connection)
    {
        echo "Error connection to database: ".$connection->connect_errno.PHP_EOL;
        exit(1);
    }
    echo "Connection established to database".PHP_EOL;
    return $connection;

}