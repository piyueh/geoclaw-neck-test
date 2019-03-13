! qinit routine for parabolic bowl problem, only single layer
subroutine qinit(meqn, mbc, mx, my, xlower, ylower, dx, dy, q, maux, aux)
    implicit none

    ! Subroutine arguments
    integer, intent(in) :: meqn, mbc, mx, my, maux
    real(kind=8), intent(in) :: xlower, ylower, dx, dy
    real(kind=8), intent(inout) :: q(meqn, 1-mbc:mx+mbc, 1-mbc:my+mbc)
    real(kind=8), intent(inout) :: aux(maux, 1-mbc:mx+mbc, 1-mbc:my+mbc)

    ! Other storage
    integer :: i, j
    real(kind=8) :: rx2, ry2

    ! initialize the q array
    q = 0D0
    
    do i=1-mbc,mx+mbc

        rx2 = xlower + (i - 0.5d0) * dx - 20D0
        rx2 = rx2 * rx2

        do j=1-mbc,my+mbc

            ry2 = ylower + (j - 0.5d0) * dy - 30D0
            ry2 = ry2 * ry2

            if ((rx2 + ry2) <= 25D0) then
                q(1, i, j) = 0.2D0
            endif
        enddo
    enddo
    
end subroutine qinit
