using Dates
using ZMQ


function sniff()
    ctx = Context(1)
    s1  = Socket(ctx, PULL)
    connect( s1, "tcp://localhost:5555")
    
    while true
        msg = recv( s1 )
        print( unix2datetime(time()), "    " )
        for i in 1:length( msg )
            @printf( "%02x ", msg[i] )
        end
        println()
    end
end

sniff()