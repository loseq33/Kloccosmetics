package pl.klocc.kloccosmetics;

/** Dodatkowe dane doklejane (mixinem) do PlayerEntityRenderState. */
public interface KloccStateAccess {
    WingType klocc$getWings();

    boolean klocc$isSneaking();

    float klocc$getTime();

    void klocc$set(WingType wings, boolean sneaking, float time);
}
